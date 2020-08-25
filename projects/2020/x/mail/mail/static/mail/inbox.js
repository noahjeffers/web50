document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#display-view').style.display = 'none';


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#display-view').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  get_mail(mailbox);
}

function get_mail(mailbox) {

  //Clears display-view 
  if(document.querySelector(".header")){
    document.querySelector("#display-view").removeChild(document.querySelector(".header"));
    document.querySelector("#display-view").removeChild(document.querySelector(".body"));
    document.querySelector("#display-view").removeChild(document.querySelector(".buttons"));
  }
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails =>{

    // If promise is empty
    if(emails<1){
      const notification = "This folder is empty";
      const element = document.createElement('div');        
      document.querySelector("#emails-view").append(notification);
    }
    else{
      emails.forEach(email=>console.log(email.sender));
      emails.forEach(email=>{
        const element = document.createElement('div');
        if (email.read == true){
          element.className = "email-read";
        }
        else{
          element.className = "email-new";
        }        
        element.innerHTML = `<p><span class="left">Subject: ${email.subject}</span><span class="center">${email.sender}</span><span class="right">${email.timestamp}</span></p>`;
        document.querySelector("#emails-view").append(element);
        if(mailbox=='inbox'){
          element.addEventListener('click', function(){read(email.id)});
        }
        else{
          element.addEventListener('click', function(){open_email(email.id)});
        }
      });
    }
  });
}

function read(email_id){
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })  
  open_email(email_id);
}

function open_email(email_id){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#display-view').style.display = 'block';
  console.log(email_id)
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    const header = document.createElement('div');
    header.className="header";
    header.innerHTML=`<p>From: ${email.sender}<small id="display-date">On: ${email.timestamp}</small></p>`;
    header.innerHTML+=`<p>To: ${email.recipients}</p>`;
    header.innerHTML+=`<p>To: ${email.subject}</p>`;
    
    const body = document.createElement('div');
    body.className="body";
    body.innerHTML=`<p>${email.body}</p>`;


    const buttons = document.createElement('div');
    buttons.className="buttons";
    buttons.innerHTML='<button id="reply" type="button" class="btn btn-success">Reply</button>';
    
    if(email.archived==false){
      buttons.innerHTML+='<button id="archive" type="button" class="btn btn-info">Archive</button>';
    }
    else{
      buttons.innerHTML+='<button id="unarchive" type="button" class="btn btn-info">Remove from Archive</button>';
    }
    


    document.querySelector("#display-view").appendChild(header);
    document.querySelector("#display-view").appendChild(body);
    document.querySelector("#display-view").appendChild(buttons);

    if(document.querySelector("#archive")){
      document.querySelector("#archive").addEventListener('click',function(){archive(email.id,true)});
    }
    else{
      document.querySelector("#unarchive").addEventListener('click',function(){archive(email.id,false)});
    }   
   
    document.querySelector("#reply").addEventListener('click',function(){});


    //Add Buttons
  });
}

function archive(email_id,archive){
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: archive
    })
  })
  // load_mailbox('inbox');
  get_mail('inbox');
  document.getElementById('inbox').click();

}
