from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from django.contrib import messages
import random
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    for this_entry in util.list_entries():
        if this_entry.upper() == entry.upper():
            return render(request,"encyclopedia/entry.html", {
                "entry_detail": markdown_to_html(util.get_entry(this_entry)),
                "entry": this_entry
            })

    return render(request,"encyclopedia/entry.html", {
    "entry_detail": "Error: no such an entry"
    })

def search(request):
    if request.method =="GET":
        searched=request.GET.get('q')

        #if there is an exact match of the searched, redirect to the entry's page;
        for entry in util.list_entries():
            if entry.upper() == searched.upper():
                return HttpResponseRedirect(reverse("entry", args=(entry,)))

            # elif the search is a substring of the entries, return a page with all the entries ( with link)
        search_result = []
        for entry in util.list_entries():
            entry_upper = entry.upper()
            temp = set([entry_upper[i:j] for i in range(len(entry_upper)) for j in range(i, len(entry_upper) + 1)])
            if searched.upper() in temp:
                search_result.append(entry)

        return render(request,"encyclopedia/search.html", {
            "entries": search_result
            })

def newpage(request):
    return render(request, "encyclopedia/newpage.html", {})

def message(request):
    return render(request, "encyclopedia/message.html", {})

def newentry(request):
    if request.method =="POST":
        title = request.POST["title"]
        content = request.POST["content"]

        entry_set = set()
        for entry in util.list_entries():
            entry_set.add(entry.upper())


        if title.upper() in entry_set:
            return render(request, "encyclopedia/message.html", {
                    "messages": f" {title} already exists in Wiki database."
                })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=(title,)))

# def editpage(request):
#     return render(request, "encyclopedia/editpage.html", {})

def edit_entry(request,entry):
    if request.method == "GET":
        if entry:
            entry_detail = util.get_entry(entry)
            return render(request, "encyclopedia/editpage.html", {
                "entry": entry,
                "content": entry_detail
            })

    if request.method =="POST":
        title = request.POST["title"]
        content = request.POST["content"]

        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=(title,)))
        # return render(request, "encyclopedia/entry.html", {
        #         "entry": title,
        #         "content": util.get_entry(title)
        #     })

def random_page(request):
    saved_entries = util.list_entries()
    random_int = random.randint(0, len(saved_entries) - 1)
    random_entry = saved_entries[random_int]
    return HttpResponseRedirect(reverse("entry", args=(random_entry,)))

    # return render(request, "encyclopedia/entry.html", {
    #     "entry": random_entry,
    #     "content": util.get_entry(random_entry)
    # })


def markdown_to_html(content):
    markdowner = Markdown()
    return markdowner.convert(content)
