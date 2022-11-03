from django.contrib import admin
from .models import Post, Section, Comment
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'date_publish', 'status')
    list_filter = ('status', 'date_create', 'date_publish', 'author')
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)
    date_hierarchy = 'date_publish'
    ordering = ('status', 'date_publish')

admin.site.register(Section)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date_create', 'active')
