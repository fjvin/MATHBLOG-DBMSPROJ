from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    """ The home page for the MathBlog. """
    return render(request, 'blog_QA/index.html')


@login_required
def topics(request):
    """ Show all topics. """
    topics = Topic.objects.order_by('-date_added')
    context = {'topics': topics}
    return render(request, 'blog_QA/topics.html', context)


@login_required
def topic(request, topic_id):
    """ Show a single topic and its entries. """
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'blog_QA/topic.html', context)


@login_required
def new_topic(request):
    """ Add a new topic. """
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('blog_QA:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blog_QA/new_topic.html', context)


@login_required
def entries(request, topic_id):
    """ See all the entries to a topic or Add a new entry """
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('date_added')

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
        
    # Display a blank form or invalid form.
    context = {'topic': topic, 'entries': entries, 'form': form}
    return render(request, 'blog_QA/entries.html', context)


@login_required
def edit_topic(request, topic_id):
    """ Edit an existing topic. """
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = TopicForm(instance=topic)
    else:
        # POST data submitted; process data
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_QA:topics')
    
    # Display a blank form or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'blog_QA/edit_topic.html', context)


@login_required
def edit_entry(request, entry_id):
    """ Edit an existing entry. """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Make sure the topic belongs to the current user.
    if entry.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submimtted; process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_QA:entries', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'blog_QA/edit_entry.html', context)


@login_required
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    if request.method == 'POST':
        # Delete confirmed
        topic.delete()
        return redirect('blog_QA:topics')

    context = {'topic': topic}
    return render(request, 'blog_QA/delete_topic.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Make sure the topic belongs to the current user.
    if entry.owner != request.user:
        raise Http404

    if request.method == 'POST':
        # Delete confirmed
        entry.delete()
        return redirect('blog_QA:entries', topic.id)

    context = {'entry': entry, 'topic': topic}
    return render(request, 'blog_QA/delete_entry.html', context)

@login_required
def owned_topics(request):
    """ Show all owned topics. """
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    context = {'topics': topics}
    return render(request, 'blog_QA/owned_topics.html', context)
