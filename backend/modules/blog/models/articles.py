from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from pytils.translit import slugify
from modules.system.services.utils import ImageDirectorySave
from modules.system.services.utils import unique_slugify
from django.urls import reverse

class Article(models.Model):
	# Модель статей
	title = models.CharField(verbose_name='Заголовок', max_length=255)
	slug = models.SlugField	(verbose_name='URL', max_length=255, blank=True)
	category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='articles', verbose_name='Категория')
	short_description = models.TextField(verbose_name='Краткое описание', max_length=300)
	full_description = models.TextField(verbose_name='Описание')
	author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT, related_name='article_author') 
	created_at = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True, db_index=True)
	is_published = models.BooleanField(verbose_name='Опубликовано', default=True)
	thumbnail = models.ImageField(
		verbose_name='Превью поста',
		blank=True,
		upload_to=ImageDirectorySave('images/thumbnails/'),
		validators=[FileExtensionValidator(
		allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))
		]
	)

	class Meta:
		# Сортировка и отображение
		ordering = ('-created_at',)
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'
		db_table = 'app_posts'

	def __str__(self):
		# Строковое представление
		return self.title

	@property
	def get_thumbnail(self):
		# Получение заглушки при отсутствии изображения
		if not self.thumbnail:
			return '/media/images/placeholder.png'
		return self.thumbnail.url
	
	def save(self, *args, **kwargs):
		# Сохранение незаполненных полей
		if not self.slug:
			self.slug = unique_slugify(self, self.title)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('article-detail', kwargs={'slug': self.slug})