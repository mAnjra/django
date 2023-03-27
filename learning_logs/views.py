from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy


# Create your views here.

def index(request):
    '''The homepage for learning logs'''
    if request.user.is_authenticated:
        topic_counts = Topic.objects.filter(owner=request.user)
        #context = {'topic_count':topic_count}
        context = {'topic_count':topic_counts}
        return render(request, 'learning_logs/index.html', context)
    else:
        return render(request, 'learning_logs/index.html')

# topics function needs to retrive some data from the database and send it to the template
 # decorator will tell python to run login_required code before function
# the code in longin required checks to see if the user is logged in - and only run the function topic if the user is
# if not theyre sent to the login page.
@login_required
def topics(request):
    '''Show all topics'''
    # topics = Topic.objects.order_by('date')  # database query
    # the above will be edited to add a filter for owner based topics
    topics = Topic.objects.filter(owner=request.user).order_by('date')
    entry_count = Topic.objects.filter(owner=request.user).annotate(total_post=Count('entry'))

    context = {'topics': topics, 'entry_count': entry_count, 'jip': zip(topics, entry_count)}

    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    '''Show a single topic and all its entries'''
    #QUERIES - best to try these out in the Django shell to see if they work
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topics belong to the current user
    #page_not_found()
    #if topic.owner != request.user: # does the topic being requested match the person currently logged in?
    #    raise Http404
    page_not_found(topic.owner, request)

    entries = topic.entry_set.order_by('-date_added')

    context = {'topic': topic, 'entries': entries}

    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    '''Add a new topic'''
    if request.method != 'POST':
        #No data submitted. create a blank form
        form = TopicForm()
    else:
        # POST data submitted. process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            # before there was only form.save() now we need to make sure new topics owner field has current logged in user feild added
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    #Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    '''Add a new entry for a particular topic'''
    topic = Topic.objects.get(id=topic_id) # querying DB to get ID topic now equals topic id from user request
    page_not_found(topic.owner, request)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
         new_entry = form.save(commit=False)
         new_entry.topic  = topic
         new_entry.save()
         return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'topic':topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    '''Taking entry and editing it'''
    #query the database
    entry = Entry.objects.get(id=entry_id)

    topic = entry.topic # get the topic associated with the entry
    page_not_found(topic.owner, request)

    if request.method != 'POST':
        form = EntryForm(instance=entry) # create the form prefilled with info from current entry
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)

def page_not_found(owner, request):
    '''Check to see if the requested page is associated with the owner'''
    if owner != request.user:
        raise Http404

@login_required
def delete_entry(request, entry_id):
    """Deletes entry and returns to topic page"""
    # get the right entry
    entry = Entry.objects.get(id=entry_id)

    #topic that is associated with entry so we can return
    topic = entry.topic

    # delete topic
    entry.delete()
    return redirect('learning_logs:topic', topic_id=topic.id)

def delete_topic(request, topic_id):
    """deletes topic and returns to topic page"""
    # gets right topic
    topic = Topic.objects.get(id=topic_id).delete()
    return redirect('learning_logs:topics')


@login_required
def search(request):

    if request.method == "POST":
        searched = request.POST['searched'] # search bar has been given name= attribute, we can reference that in the view so whatever user types in is now in searched
        #result = Entry.objects.filter(text__contains=searched) this brings up entries from all users
        # here we use q objects that allow us to complex searches
        result = Entry.objects.annotate(search=SearchVector('text')).filter(Q(topic__owner=request.user), Q(search=searched)).order_by('-date_added')

        #result = Entry.objects.annotate(search=SearchVector('text').filter(text__contains=searched)
        return render(request, 'learning_logs/search_logs.html', {'searched':searched, 'result':result})
    else:
        return render(request, 'learning_logs/search_logs.html', {})



def topic_delete(DeleteView):
    topic = Topic.objects.get(id=topic_id)
    success_url = reverse_lazy('topics')
