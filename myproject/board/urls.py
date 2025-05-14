from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.home , name = 'home'),
    path('board/<int:pk>',views.board_topics, name = "board_topics" ),
    path('board/<int:pk>/new', views.new_topics, name = "new_topics"),
    path('board/<int:pk>/topics/<int:topic_pk>/', views.topic_posts, name='topic_posts'),

]
