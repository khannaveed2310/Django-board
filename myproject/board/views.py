from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Board, Topic, Post
from django.contrib.auth.decorators import login_required



def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    board = Board.objects.filter(pk=pk).first()
    return render(request, 'topics.html' , {'board' : board})

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

        return redirect('board_topics', pk = board.pk)
    
    return render(request, 'new_topics.html', {'board': board})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})