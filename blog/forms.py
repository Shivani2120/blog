from django import forms
from .models import Comment
from .models import BlogPost

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']

class BlogForm(forms.ModelForm):  
    class Meta:  
        model = BlogPost  
        fields = "__all__"  