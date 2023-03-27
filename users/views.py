from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register(request):
    """Register a new user"""
    if request.method != 'POST':
        #Display blank form
        form = UserCreationForm()
    else:
        #Process completed form.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Log the user in then - redirect to homepage - why its saved in variable

            login(request, new_user)
            return redirect('learning_logs:index')

    context = {'form' : form}
    return render(request, 'registration/register.html', context)
