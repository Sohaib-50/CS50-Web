from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    if (contents := util.get_entry(title)):
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "contents": contents
        })
    else:
        return render(request, "encyclopedia/wiki_unavailable.html", {
            "title": title
        }
        )
