from django.urls import path
from modules.blog.views.articles import ArticleListView

urlpatterns = [
	path('', ArticleListView.as_view(), name='article-list'),
]