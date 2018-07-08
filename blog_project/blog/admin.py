from django.contrib import admin

from .models import Post, Comment, Feed, Article


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Feed)
admin.site.register(Article)
