from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from youtubesearchpython import VideosSearch
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
    if request.method == 'POST':
        form = HomeWorkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = HomeWork(user=request.user,
                                 subject=request.POST['subject'],
                                 title= request.POST['title'],
                                 description= request.POST['description'],
                                 due= request.POST['due'],
                                 is_finished= finished,
            )
            homeworks.save()
            messages.success(request,f'Homework added from {request.user.username} !!!')
    else:
        form = HomeWorkForm()
    hw = HomeWork.objects.filter(user=request.user)
    if len(hw) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        "homeworks":hw,
        "homework_done":homework_done,
        "form":form,
    }
    return render(request, 'dashboard/homework.html', context)


def update_homework(request, pk=None):
    hw = HomeWork.objects.get(id=pk)
    if hw.is_finished:
        hw.is_finished = False
    else:
        hw.is_finished = True
    hw.save()
    return redirect('homework')


def delete_homework(request, pk=None):
    HomeWork.objects.get(id=pk).delete()
    return redirect("homework")



def youtube(request):
    if request.method == 'POST':
        form = DashBoardForm()
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],

            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']

            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request, 'dashboard/youtube.html',context)
    else:
        form = DashBoardForm()
    context = {
        "form":form
    }
    return render(request, 'dashboard/youtube.html', context)


