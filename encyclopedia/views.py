from django.shortcuts import render, redirect
from .util import get_entry, list_entries, save_entry
from django.http import Http404, HttpResponse
from django.urls import reverse
import random

import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry_md = get_entry(title)
    if entry_md is not None:
        entry_html = markdown2.markdown(entry_md)
        return render(request, 'wiki/entry.html', {'entry_html': entry_html, 'title': title})
    else:
        raise Http404("Entry not found")


def search(request):
    query = request.GET.get('q', '')
    entry_md = get_entry(query)

    if entry_md is not None:
        return redirect('entry', title=query)
    
    entries = list_entries()
    resulting_entries = []

    for entry in entries:
        if query.lower() in entry.lower():
            resulting_entries.append(entry)

    return render(request, 'wiki/search.html', { 'query': query, 'entries': resulting_entries })

def new_entry(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        existing_entry = get_entry(title)

        if existing_entry is not None:
            return HttpResponse("An entry with this title already exists. Please choose a different title.")

        if title and content:
            entry = f"# {title}\n\n{content}"
            save_entry(title, entry)
            return redirect('entry', title=title)
        else:
            return HttpResponse("Title and content are required")
    return render(request, 'wiki/new_entry.html')

def random_entry(request):
    entries = list_entries()
    random_title = random.choice(entries)
    return redirect('entry', title=random_title)

def edit(request, title):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        content = content.replace('\r\n', '\n')
        if content:
            save_entry(title, content)
            return redirect('entry', title=title)
        else:
            return HttpResponse("Content is required")
    entry_md = get_entry(title)
    return render(request, 'wiki/edit.html', {'title': title, 'content': entry_md})
