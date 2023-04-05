from django.contrib import admin
from modules.blog.models import Article, Category
from mptt.admin import DraggableMPTTAdmin

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'author')
	list_display_links = ('title', 'slug')
	prepopulated_fields = {'slug': ('title',)}

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
	list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
	list_display_links = ('title', 'slug')
	prepopulated_fields = {'slug': ('title',)}

	fieldsets = (
		('Основная информация', {'fields': ('title', 'slug', 'parent')}),
		('Описание', {'fields': ('description',)}),
	)