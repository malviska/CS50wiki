from django.shortcuts import render, redirect
from django.http import Http404
from django import forms
from . import util
from random import randint
import re

class EditEntryForm(forms.Form):
   textArea = forms.CharField(label="Markdown text", required=True, widget=forms.Textarea)

class CreateForm(forms.Form):
   title = forms.CharField(label="Title", required=True, max_length=100)
   textArea = forms.CharField(label="Markdown text",required=True, widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    getEntry = util.get_entry(entry)
    if not getEntry:
      raise Http404("Not found")        
    result = util.markdown_parser(getEntry)
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "result": result
    })

def edit(request, entry):
   getEntry = util.get_entry(entry)
   if not getEntry:
      raise Http404("Not found")
   if request.method == "POST":
      edited = request.POST.get("textArea")
      util.save_entry(entry, edited, True)
      return redirect(f'/wiki/{entry}')

   form = EditEntryForm(initial={'textArea': getEntry})
   return render(request,"encyclopedia/edit.html", {
      "title": entry,
      "form": form
   })

    
def search(request):
   if request.method == "POST":
      searched = request.POST.get('q')
      getEntry = util.get_entry(searched)
      if not getEntry:
         return render(request, "encyclopedia/search.html", {
            "entries": util.list_similar_entrys(searched)
         })
      else:
         return redirect(f'wiki/{searched}')
      
def create(request):
  isNameError = False
  if request.method == "POST":
      title = request.POST.get("title")
      newEntry = request.POST.get('textArea')
      try: 
        util.save_entry(title, newEntry, False)
        return redirect(f'wiki/{title}') 
      except NameError:
         isNameError = True

  return render(request, "encyclopedia/create.html", {
      "form": CreateForm(),
      "isNameError": isNameError
   })

def random(request):
     entries = util.list_entries()
     val = randint(0, len(entries) -1)
     match = re.search(r'"(.*)"', entries[val])
     return redirect(match.group(1))