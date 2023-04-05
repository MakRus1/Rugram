import time
from pathlib import Path
from uuid import uuid4
from pytils.translit import slugify

from django.utils.deconstruct import deconstructible

@deconstructible
class ImageDirectorySave(object):
	# Класс загрузчика в определенную директорию
	def __init__(self, save_path):
		self.path = save_path

	def __call__(self, instance, filename):
		ext = filename.split('.')[-1]

		if instance and hasattr(instance, 'slug'):
			filename = f'img-{instance.slug}.{ext}'
		else:
			filename = f'img-{uuid4().hex}.{ext}'
		path = Path(self.path, time.strftime('%Y/%m/%d'), filename)
		return path

def unique_slugify(instance, slug):
	model = instance.__class__
	unique_slug = slugify(slug)
	while model.objects.filter(slug=unique_slug).exists():
		unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
	return unique_slug