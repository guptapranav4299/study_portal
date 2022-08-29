from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .models import *
from .forms import *

# Create your views here.


def home(request):
    return render(request,'dashboard/home.html')


def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes added from {request.user.username} successfully!!")
    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)
    context = {
        'notes':notes,
        'form':form,
    }
    return render(request,'dashboard/notes.html',context)


def delete_notes(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDetailsView(DetailView):
    model = Notes


def homework(request):
    return render(request, 'dashboard/homework.html')