from django.contrib import admin
from .models import Post, Author, Category, Comment


class BlogAdmin(admin.ModelAdmin):
    class Media:
        js = ("js/script.js",)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address', 'phone',
                    'field_of_study', 'blog_category')
    ordering = ('name', 'email', 'address', 'phone',
                    'field_of_study', 'blog_category')
    search_fields = ('name', 'email', 'address', 'phone',
                    'field_of_study', 'blog_category')
    list_filter = ('name', 'email', 'address', 'phone',
                    'field_of_study', 'blog_category')
    
admin.site.register(Post, BlogAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Comment)