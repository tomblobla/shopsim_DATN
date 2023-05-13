from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Topic, Post


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'desc', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    inlines = [PostInline]

    def post_count(self, obj):
        return obj.posts.count()

    post_count.short_description = 'Số bài viết'
    
    
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'is_pinned')
    list_filter = ('topic', 'is_pinned')
    search_fields = ('title', 'content')

    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
