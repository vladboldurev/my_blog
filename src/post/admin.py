from django.contrib import admin

from .models import Category, Post, Comment, HashTag
from .forms import PostForm


class PostAdmin(admin.ModelAdmin):
    add_form = PostForm
    form = PostForm
    model = Post

    list_display = ('id', 'title', 'overview', 'author', 'timestamp',
                    'thumbnail', 'featured', 'content',
                    'prev_post', 'next_post')
    list_filter = ('title', 'overview', 'author', 'timestamp',
                   'thumbnail', 'category', 'featured', 'content',
                   'prev_post', 'next_post')
    fieldsets = (
        (None, {'fields': ('title', 'overview', 'author',
                           'thumbnail', 'featured', 'content',
                           'prev_post', 'next_post')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'overview', 'author', 'timestamp',
                       'thumbnail', 'category', 'featured', 'content',
                       'prev_post', 'next_post')}
         ),
    )
    search_fields = ('title',)
    ordering = ('title',)

admin.site.register(Post, PostAdmin)

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(HashTag)
