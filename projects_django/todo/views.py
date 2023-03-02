from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Todo
from .forms import TodoForm

# Create your views here.
#
#def index(request):
 #   "Show todays Todo"
  #  todo = Todo.objects.filter(my_boolean_field=False)
   # todo_title = Todo.objects.get()
    #context = {'todo': todo, 'title':}
    #return render(request, 'todo/todo_main.html', context)

def index(request):
    "Show today's Todo"
    todo = Todo.objects.filter(my_boolean_field=False)
    todo_title = todo.first()
    todo_fields = todo.values('date','title')
    if request.method != 'POST':
        # create a blank form
        form = TodoForm()
    else:
        form = TodoForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    context = {'todo': todo, 'title': todo_title.date if todo_title else None,'date':todo_fields,'form':form}
    return render(request, 'todo/todo_main.html', context)   

def add_todo(request):
    "add new todo for"
    if request.method != 'POST':
        # create a blank form
        form = TodoForm()
    else:
        form = TodoForm(data=request.POST)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'todo/todo_main.html', context)
