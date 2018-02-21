from django.contrib import admin
from . import models

# Register your models here.


# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'created_on')
#     search_fields = ['name', 'email']
#     ordering = ['-name']
#     list_filter = ['active']
#     date_hierarchy = 'created_on'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author', 'category',)
    search_fields = ['title', 'content']
    ordering = ['-pub_date']
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    # filter_horizontal = ('tags',)
    raw_id_fields = ('tags',)
    # prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('slug',)
    fields = ('title', 'slug', 'content', 'author', 'category', 'tags',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','date',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Category, CategoryAdmin)
# admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Author)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Feedback, FeedbackAdmin)
