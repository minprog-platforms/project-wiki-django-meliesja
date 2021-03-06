
from django.shortcuts import redirect, render
from markdown2 import Markdown
from django import forms
from . import util
import random

class CreateForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")

def index(request):
    """
    Displays index (home) page.
    """
    # display all entries in list 
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })

def entry(request, title):
    """
    Displays selected entry page if it exists, otherwise displays error page.
    """
    # create variable to store retrieved entry
    entry_page = util.get_entry(title)

    markdown = Markdown()
    
    if entry_page is not None:
        # display entry content 
        return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown.convert(entry_page)
        })

    # display error page
    return render(request, "encyclopedia/error.html", {
        "title": title
        })

def search(request):
    """
    Displays searched page if it exists, otherwise displays search results.
    """
    query = request.GET.get("q")

    if util.get_entry(query) is not None:
        return redirect(entry, query)

    entries = util.list_entries()
    
    results = []

    # add pages similar to query to list
    for page in entries:
        if query.upper() in page.upper():
            results.append(page)

    # return related results
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
        })   

def new(request):
    """
    Creates new wiki page and redirects user to that page.
    """
    if request.method == "POST":
        form = CreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            
            content = form.cleaned_data["content"]

            # add markdown syntax to store contents correctly
            new_content = f"#{title}\n\n{content}"

            util.save_entry(title, new_content)
            
            # redirect user to newly created page
            return redirect("entry", title)

    # return empty form
    return render(request, "encyclopedia/new.html", {
        "form": CreateForm()
        })
        
def random_page(request):
    """
    Redirects user to a random wiki page.
    """
    # store all entry titles in variable
    entries = util.list_entries()

    # choose random entry
    random_entry = random.choice(entries)

    return redirect(entry, random_entry)
    