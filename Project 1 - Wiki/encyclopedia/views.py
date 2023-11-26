from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):

    # if entry exists
    if (content := util.get_entry(title)):
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "contents": util.markdown_to_html(content)
        })
    
    # if entry does not exist
    else:
        return render(request, "encyclopedia/error.html", {
            "error_message": f"No wiki entry for {title} found."
        })

    
def search(request):
    query = request.GET.get("q").strip().lower()  # get query  # TODO: handle empty query
    entries = [entry.lower() for entry in util.list_entries()]

    # if query appears exactly in entries, then redirect to wiki page of the query
    if query in entries:
        return HttpResponseRedirect(reverse("encyclopedia:wiki", args=(query,)))
    
    # find all non exact matches of query, i.e. substrings.
    non_exact_matches = []
    for entry in entries:
        if query in entry:
            non_exact_matches.append(entry)

    return render(request, "encyclopedia/search.html", {
        "search_results": non_exact_matches
    })
    
def new(request):
    # if visiting to create a new page
    if request.method == "GET":
        return render(request, "encyclopedia/page_form.html", {
            "creating_new": True,
            "page_title": "Create Page"
        })
    
    # if visiting after submitting a new page
    else:
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        print(title, content)

        
        # check if entry already exsists
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                # error message with link to existing entry
                "error_message": f"Entry for <a href='{reverse('encyclopedia:wiki', args=(title,))}'>{title}</a> already exists."
            })
            
        # save new entry
        util.save_entry(title, content)

        return HttpResponseRedirect(reverse("encyclopedia:wiki", args=(title,)))    
    

def random_page(request):
    all_titles = util.list_entries()
    random_title = random.choice(all_titles)
    return HttpResponseRedirect(reverse("encyclopedia:wiki", args=(random_title,)))


def edit(request, title):
    if request.method == "GET":
        print({
            "creating_new": False,
            "page_title": "Edit Page",
            "title": title,
            "content": util.get_entry(title)
        })
        return render(request, "encyclopedia/page_form.html", {
            "creating_new": False,
            "page_title": "Edit Page",
            "title": title,
            "content": util.get_entry(title)
        })
    
    # POST request
    else:
        new_content = request.POST.get("content")
        util.save_entry(title=title, content=new_content)
        return HttpResponseRedirect(reverse("encyclopedia:wiki", args=(title,)))    
