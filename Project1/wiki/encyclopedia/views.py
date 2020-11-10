from django.shortcuts import render
from django.http import HttpResponse

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    if name in util.list_entries():
        markeddown = markdown2.markdown(util.get_entry(name))
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "entry": markeddown
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "name" : name,
            "entry" : "<h2>Your requested page was not found</h2>"
        })
