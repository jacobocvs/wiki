from django.shortcuts import render, redirect
from .util import get_entry, list_entries, save_entry
from django.http import Http404, HttpResponse
from django.urls import reverse

import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry_md = get_entry(title)
    if entry_md is not None:
        entry_html = markdown.markdown(entry_md)
        return render(request, 'wiki/entry.html', {'entry_html': entry_html, 'title': title})
    else:
        raise Http404("Entry not found")


def search(request):
    query = request.GET.get('q', '')
    entry_md = get_entry(query)

    if entry_md is not None:
        return redirect(
            reverse('entry', kwargs={'title': query})
        )
    
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
        entry = f"# {title}\n\n{content}"

        if title and content:
            save_entry(title, entry)
            return redirect('entry', title=title)
        else:
            return HttpResponse("Invalid form submission. Title and content are required")
    return render(request, 'wiki/new_entry.html')
