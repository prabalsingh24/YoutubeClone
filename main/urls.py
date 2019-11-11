from django.contrib import admin
from django.urls import path
from .views import HomeView,LoginView,RegisterView,AddVideo,DetailedVideo,CommentView

urlpatterns = [
    path('', HomeView.as_view()),
    path('login/',LoginView.as_view()),
    path('register/',RegisterView.as_view()),
    path('addVideo/',AddVideo.as_view()),
    path('video/<id>/',DetailedVideo.as_view()),
    path('addComment/',CommentView.as_view())
]