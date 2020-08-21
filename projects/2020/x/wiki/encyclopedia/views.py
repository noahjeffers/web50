from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from random import randint

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html",{
            "error":"This page doesn't exist"
        })
    else:
        topic = util.get_entry(title)
        markdowner = Markdown()
        return render(request, "encyclopedia/page.html",{
            "topic" : markdowner.convert(topic),
            "title": title.capitalize()
        })

def new(request):
    if request.method == "POST":
        title = request.POST.get("title","")
        content = request.POST.get("content", "")
        markdowner = Markdown()
        if util.get_entry(title) != None:
            return render(request,"encyclopedia/error.html",{
                "error":"This page already exists"
            })
        else:            
            util.save_entry(title,content)   
            return redirect('/wiki/'+title)  

    return render(request,"encyclopedia/newpage.html")

def edit(request, title):
    if request.method == "POST":
        oldtitle = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(oldtitle, content)
        return redirect('/wiki/'+title)
    content = util.get_entry(title)
    return render(request,"encyclopedia/edit.html",{
        "title":title,
        "content" : content
    })

def search(request):
    lst = []
    title = request.GET['q']
    markdowner = Markdown()
    if util.get_entry(title) != None:
        return render(request, "encyclopedia/page.html",{
            "title": title,
            "topic": markdowner.convert(util.get_entry(title))
        })
    else:
        for word in util.list_entries():
            if title.lower() in word.lower():
                lst.append(word)
        if len(lst) > 0:
            return render(request, "encyclopedia/results.html",{
                "entries" : lst
            })
        else:
            return render(request, "encyclopedia/error.html",{
                "error" : "There are no pages that match that search"
            })

def random(request):
    markdowner = Markdown()
    entries = util.list_entries()
    choice = randint(0,(len(entries)-1))
    selection = entries[choice]
    return redirect('/wiki/'+selection)

def error(request):
    return render(request, "encyclopedia/error.html")