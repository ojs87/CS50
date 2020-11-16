from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.core.exceptions import ValidationError
import random

from . import util
import markdown2

class NewSearchForm(forms.Form):
    search=forms.CharField(label="Search Encyclopedia")

def validate_title(value):
    if value.upper() not in (entry.upper() for entry in util.list_entries()):
        return value
    else:
        raise ValidationError("This entry already exists")

class CreatePageForm(forms.Form):
    page_title=forms.CharField(label="Title", validators=[validate_title])
    page_content=forms.CharField(label="Content", widget=forms.Textarea)

class EditPageForm(forms.Form):
    page_content=forms.CharField(label="Content", widget=forms.Textarea)


def index(request):
    if request.method == "POST":
        form=NewSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            if search.upper() in (entry.upper() for entry in util.list_entries()):
                markeddown= markdown2.markdown(util.get_entry(search))
                return render(request, "encyclopedia/entry.html", {
                    "name" : search,
                    "entry": markeddown,
                    "form": NewSearchForm()
                    })
            else:
                return render(request, "encyclopedia/searchresults.html", {
                    "form" : NewSearchForm(),
                    "entries" : util.list_entries(),
                    "searchresult" : search
                    })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": form
                })

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewSearchForm()
    })

def entry(request, name):
    if request.method == "POST":
        form=request.POST
        content=form["page_content"]
        util.save_entry(name, content)
        return HttpResponseRedirect(name)
    if name in util.list_entries():
        markeddown = markdown2.markdown(util.get_entry(name))
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "entry": markeddown,
            "form": NewSearchForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "name" : name,
            "entry" : "<h2>Your requested page was not found</h2>",
            "form": NewSearchForm()
        })

def newpage(request):
    if request.method == "POST":
        form=CreatePageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["page_title"]
            content = form.cleaned_data["page_content"]
            util.save_entry(title, content)
            return HttpResponseRedirect("wiki/" + title)
        else:
            return render(request, "encyclopedia/createnewpage.html", {
                "form2" : form,
                "form" : NewSearchForm()
                })
    else:
        return render(request, "encyclopedia/createnewpage.html", {
            "form": NewSearchForm(),
            "form2": CreatePageForm()
    })

def editpage(request, name):
    #extra lines added to textarea, had to use .replace() to get rid of the \r
    entry=util.get_entry(name).replace('\r', '')
    markeddown = markdown2.markdown(util.get_entry(name))
    data= {'page_content': entry}
    return render(request, "encyclopedia/editpage.html", {
            "form": NewSearchForm(),
            "entry": entry,
            "name": name
    })

def randompage(request):
    entry=random.choice(util.list_entries())
    return HttpResponseRedirect(entry)
