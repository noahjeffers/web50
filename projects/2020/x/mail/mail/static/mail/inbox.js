document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  compose();
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
  // get_mail(mailbox);
  if(document.querySelector(".header")){
    document.querySelector("#display-view").removeChild(document.querySelector(".header"));
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
      emails.forEach(email=>{
        const element = document.createElement('div');
        if(mailbox=='inbox'){
          if (email.read == true){
            element.className = "email-read";
          }
          else{
            element.className = "email-new";
          }  
        }
        else{
          element.className = "email-read";
        }
        element.innerHTML = `<p><span class="left">Subject: ${email.subject}</span><span class="center">${email.sender}</span><span class="right">${email.timestamp}</span></p>`;
        document.querySelector("#emails-view").append(element);

        element.addEventListener('click', function(){open_email(email.id,mailbox)});
      });
    }
  });
}

// function get_mail(mailbox) {

//   //Clears display-view 
//   if(document.querySelector(".header")){
//     document.querySelector("#display-view").removeChild(document.querySelector(".header"));
//   }
//   fetch(`/emails/${mailbox}`)
//   .then(response => response.json())
//   .then(emails =>{

//     // If promise is empty
//     if(emails<1){
//       const notification = "This folder is empty";
//       const element = document.createElement('div');        
//       document.querySelector("#emails-view").append(notification);
//     }
//     else{
//       emails.forEach(email=>{
//         const element = document.createElement('div');
//         if (email.read == true){
//           element.className = "email-read";
//         }
//         else{
//           element.className = "email-new";
//         }        
//         element.innerHTML = `<p><span class="left">Subject: ${email.subject}</span><span class="center">${email.sender}</span><span class="right">${email.timestamp}</span></p>`;
//         document.querySelector("#emails-view").append(element);
//         if(mailbox=='inbox'){
//           element.addEventListener('click', function(){read(email.id)});
//         }
//         else{
//           element.addEventListener('click', function(){open_email(email.id,mailbox)});
//         }
//       });
//     }
//   });
// }
//Mark as Read
function read(email_id){
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })  
}

function open_email(email_id, mailbox){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#display-view').style.display = 'block';
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    read(email_id);
    const header = document.createElement('div');
    header.className="header";
    header.innerHTML=`<p>From: ${email.sender}<small id="display-date">On: ${email.timestamp}</small></p>`;
    header.innerHTML+=`<p>To: ${email.recipients}</p>`;
    header.innerHTML+=`<p id="subject">To: ${email.subject}</p>`;
    
    const body = document.createElement('div');
    body.className="body";
    body.innerHTML=`<p>${email.body}</p>`;    

    document.querySelector("#display-view").appendChild(header);
    header.appendChild(body);

  //Add Buttons
    let replyButton = document.createElement("button");
    replyButton.innerHTML="Reply";
    replyButton.addEventListener('click',()=>{reply(email.sender, email.subject, email.body,email.timestamp)})
    replyButton.className="btn btn-primary";
    replyButton.id = "reply";
    header.appendChild(replyButton);

  
    if(mailbox !='sent'){
      let archiveButton = document.createElement("button");
      if(email.archived == false){
        archiveButton.innerHTML="Archive";
        archiveButton.addEventListener('click',()=>{archive(email.id,true)})
      }
      else{
        archiveButton.innerHTML="Remove from Archive";
        archiveButton.addEventListener('click',()=>{archive(email.id,false)})
      }
      archiveButton.className="btn btn-info";
      header.appendChild(archiveButton);
    }


  });
}

function archive(email_id,archive){

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: archive
    })
  })
  load_mailbox('inbox');
  // window.location.reload();

}


function compose(){
  const form = document.querySelector("#compose-form");
  form.onsubmit = () =>{
    let to = document.querySelector("#compose-recipients");
    let subject = document.querySelector("#compose-subject");
    let body = document.querySelector("#compose-body");
    if (body.length == 0 || to.length == 0){
      return;
    }
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: to.value,
          subject: subject.value,
          body: body.value
      })
    })
    .then(response => response.json())
    .then(result => {        
        console.log(result);
      if(result.status == 401){
        alert(`${result.error}`);
      }
      else{
        load_mailbox('sent');
      }
    });   
    return false; 
  }
}

function reply(to,subject,body,time){
  compose_email();
  subject = `Re: ${subject}`;
  document.querySelector("#compose-recipients").value = to;
  document.querySelector("#compose-subject").value = subject;
  document.querySelector("#compose-body").value = ` \n\n\nOn ${time} ${to} wrote: \n${body}`;
}