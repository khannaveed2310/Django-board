from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.home , name = 'home'),
    path('board/<int:pk>',views.board_topics, name = "board_topics" ),
    path('board/<int:pk>/newtopic', views.new_topics, name = "new_topics"),
    path('board/<int:pk>/topics/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path('boards/newboard/', views.new_board, name='new_board'),


]
