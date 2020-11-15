from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import Comment, Post


class NewsAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title_text', 'author_name', 'pub_date',)
    list_display_links = ('id', 'title_text')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)