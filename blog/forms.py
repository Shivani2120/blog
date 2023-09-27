from django import forms
from .models import Comment
from .models import BlogPost

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['author', 'text']
		widgets = {
			'author': forms.TextInput(attrs={'class':'form-control', 'id': 'authodid'}),
			'text': forms.TextInput(attrs={'class':'form-control', 'id': 'textid'}),
		}

class BlogForm(forms.ModelForm):  
	class Meta:  
		model = BlogPost  
		fields = "__all__"  
		widgets = {
		  'title': forms.TextInput(attrs={'class':'form-control',
			'id': 'titleid'}),
			'content': forms.TextInput(attrs={'class':'form-control',
			'id': 'contentid'}),
			'image': forms.FileInput(attrs={'class':'form-control',
			'id': 'imageid'}),
			'pdf_file': forms.FileInput(attrs={'class':'form-control',
			'id': 'pdffileid'}),
		}