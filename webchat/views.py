from django.shortcuts import render ,get_object_or_404
from .models import Topic , Author , Book
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    #The home page
    return render(request, 'webchat/index.html')

def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics' : topics}
    return render(request,'webchat/topics.html',context)

def topic(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic , 'entries':entries}
    return render(request , 'webchat/topic.html',context)

def book_list(request):

    books = Book.objects.all()
    return render(request, 'webchat/book_list.html', {'books': books})

from django.views.generic import ListView, DetailView
from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = "webchat/article_list.html"
    context_object_name = "articles"
    paginate_by = 6

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by("-published_date")


class ArticleDetailView(DetailView):
    model = Article
    template_name = "webchat/article_detail.html"
    context_object_name = "article"
