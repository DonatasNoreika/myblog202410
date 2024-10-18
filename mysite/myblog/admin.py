from django.contrib import admin
from .models import Post, Comment


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", 'user', 'date_created']
    inlines = [CommentInLine]


admin.site.register(Post, PostAdmin)
