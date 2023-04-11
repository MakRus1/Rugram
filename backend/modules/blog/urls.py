from django.urls import path
from modules.blog.views.articles import ArticleListView, ArticleDetailView

urlpatterns = [
	path('', ArticleListView.as_view(), name='article-list'),
	path('<str:slug>/', ArticleDetailView.as_view(), name='article-detail'),
]