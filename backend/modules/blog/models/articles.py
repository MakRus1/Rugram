from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from pytils.translit import slugify
from modules.system.services.utils import ImageDirectorySave

class Article(models.Model):
	# Модель статей
	title = models.CharField(verbose_name='Заголовок', max_length=255)
	slug = models.SlugField	(verbose_name='URL', max_length=255, blank=True)
	category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='articles', verbose_name='Категория')
	short_description = models.TextField(verbose_name='Краткое описание', max_length=300)
	full_description = models.TextField(verbose_name='Описание')
	author = models.ForeignKey(User, verbose_name='Автор материала', on_delete=models.PROTECT, related_name='article_author') 
	updated_by = models.ForeignKey(User, verbose_name='Автор обновления', on_delete=models.CASCADE, related_name='article_updated_by', blank=True, null=True) 
	created_at = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True, db_index=True)
	updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True, db_index=True)
	reason = models.CharField(verbose_name='Причина обновления', max_length=100, blank=True)
	is_fixed = models.BooleanField(verbose_name='Зафиксировано', default=False, db_index=True)
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
		ordering = ('-is_fixed', '-created_at')
		verbose_name = 'Статья'
		verbose_name_plural = 'Статьи'
		db_table = 'app_articles'

	def __str__(self):
		# Строковое представление
		return self.title

	@property
	def get_thumbnail(self):
		# Получение заглушки при отсутствии изображения
		return self.thumbnail.url
	
	def save(self, *args, **kwargs):
		# Сохранение незаполненных полей
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)