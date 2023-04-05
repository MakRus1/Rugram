from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from pytils.translit import slugify

class Category(MPTTModel):
	# Модель категории с вложенностью
	title = models.CharField(verbose_name='Название категории', max_length=255)
	slug = models.SlugField(verbose_name='URL категории', blank=True)
	description = models.TextField(verbose_name='Описание категории', max_length=300)
	parent = TreeForeignKey(
		'self',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		db_index=True,
		related_name='children',
		verbose_name='Родительская категория'
	)

	class MPTTMeta:
		# Сортировка
		order_insertion_by = ('title',)

	class Meta:
		# Сортировка и отображение
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'
		db_table = 'app_categories'

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		# Сохранение незаполненных полей
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)