from django.contrib import admin
from newspaper.models import Newsletter, Post, Tag, Category,Contact, Comment
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(Newsletter)
