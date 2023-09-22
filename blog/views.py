from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import BlogPost, Comment
from .forms import BlogForm
from .forms import CommentForm

def blog_detail(request, post_id):
  blog = get_object_or_404(BlogPost, pk=post_id)
  return render(request, 'blog_detail.html', {'blog': blog})

def index(request):
  blogs = BlogPost.objects.all()
  return render(request, 'index.html', {'blogs': blogs})

def create_blog(request):
  if request.method == 'POST':
    form = BlogForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('index')
  else:
    form = BlogForm()
  return render(request, 'create_blog.html', {'form': form})

def edit_blog(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.method == 'POST':
      form = BlogForm(request.POST, instance=post)
      if form.is_valid():
        form.save()
        return redirect('index')
    else:
      form = BlogForm(instance=post)
    return render(request, 'edit_blog.html', {'form': form})

def delete_blog(request, post_id):
  blog = get_object_or_404(BlogPost, pk=post_id)
  if request.method == 'POST':
    blog.delete()
    messages.success(request,  'The blog has been deleted successfully.')
    return redirect('index')
  return redirect('blog_detail', post_id=post_id)

def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) 
            comment.post = post  
            comment.save()  
            return redirect('blog_detail', post_id=post.id)
    
    return render(request, 'blog_detail.html', {'blog': post, 'comment_form': form})

def delete_comment(request, post_id):
  comment = get_object_or_404(Comment, pk=post_id)
  if request.method == 'POST':
    comment.delete()
    messages.success(request,  'The blog has been deleted successfully.')
    return redirect('index')
  return redirect('blog_detail', post_id=comment.id)