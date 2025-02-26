"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import re_path , path ,include
from . import views
from .views import ArticleListView, ArticleDetailView

app_name = 'webchat' 

urlpatterns = [
    path('', views.index,name='index' ),
    #show all topics
    path('topics',views.topics, name='topics' ), 
    path('topics/<int:topic_id>/', views.topic, name='topic'),   
    #re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    #path('authors/', views.author_list, name='author_list'),
    #path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('books/', views.book_list, name='book_list'),
    #path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path("news/", ArticleListView.as_view(), name="article_list"),
    path("news/<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),

]

