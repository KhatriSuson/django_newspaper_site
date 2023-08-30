from django import forms
from django_summernote.widgets import SummernoteWidget

from newspaper.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("author", "published_at", "views_count")

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the title of post",
                }
            ),
            "content": SummernoteWidget(),
            "status": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "tag": forms.SelectMultiple(attrs={"calss": "form-control"}),
        }
