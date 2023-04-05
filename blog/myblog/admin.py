from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


# admin.site.register(Post, PostAdmin)
# admin.site.register(Comment, CommentAdmin)
