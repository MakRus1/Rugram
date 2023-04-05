from django.views.generic import ListView
from modules.blog.models.articles import Article

class ArticleListView(ListView):
	model = Article
	template_name = 'modules/blog/articles/article-list.html'
	context_object_name = 'articles'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Главная страница'
		return context
