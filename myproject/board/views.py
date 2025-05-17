from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Board, Topic, Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topic = board.topics.order_by('-last_updated').annotate(replies=Count('post') - 1)
    return render(request, 'topics.html' , {'board' : board, 'topic': topic})


@login_required
def new_board(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            Board.objects.create(name=name, description=description)
            return redirect('home')
    return render(request, 'new_board.html')

@login_required
def new_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()  # TODO: get the currently logged in user

        topic = Topic.objects.create(
            subject=subject,
            board=board,
            starter=request.user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=request.user
        )

        return redirect('topic_posts', pk = board.pk , topic_pk=topic.pk)
    
    return render(request, 'new_topics.html', {'board': board})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

@login_required
def reply_topic(request, pk ,topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})  


@login_required
def edit_post(request, pk, topic_pk, post_pk):
    post = get_object_or_404(Post, pk=post_pk, created_by=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_by = request.user
            post.updated_at = timezone.now()
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'post': post, 'form': form})