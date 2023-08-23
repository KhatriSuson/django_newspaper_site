from django.contrib import admin
from newspaper.models import Newsletter, Post, Tag, Category,Contact, Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(Newsletter)