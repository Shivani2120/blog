from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import BlogPost, Comment
from .forms import BlogForm
from .forms import CommentForm

def blog_detail(request, post_id):
  blog = get_object_or_404(BlogPost, pk=post_id)
  comments = Comment.objects.filter(post=blog)

  if request.method == 'POST':
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      new_comment = comment_form.save(commit=False)
      new_comment.post = blog
      new_comment.save()
      return redirect('blog_detail', post_id=blog.id)
  else:
    comment_form = CommentForm()
  return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments, 'comment_form': comment_form})

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
    blog = get_object_or_404(BlogPost, pk=post_id)

    if request.method == 'POST':
      form = CommentForm(request.POST)
      if form.is_valid():
        comment = form.save(commit=False)
        comment.post = blog
        comment.save()
        return redirect('blog_detail', post_id=blog.id)
    return render(request, 'blog_detail.html', {'blog': blog, 'comment_form': form})

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
      form = CommentForm(request.POST, instance=comment)
      if form.is_valid():
        form.save()
        return redirect('blog_detail', post_id=comment.post.id)
    else:
      form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})

def delete_comment(request, comment_id):
  comment = get_object_or_404(Comment, pk=comment_id)
  if request.method == 'POST':
    post_id = comment.post.id
    comment.delete()
    return redirect('blog_detail', post_id=post_id)
  return redirect('blog_detail', post_id=post_id)