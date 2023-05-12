from django.contrib import admin
from .models import Subject, News, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created','updated']
    list_filter = ['created', 'subject','updated']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
