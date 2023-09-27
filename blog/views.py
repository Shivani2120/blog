from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import BlogPost, Comment, Like
from .forms import BlogForm
from .forms import CommentForm
import pdb;
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def blog_detail(request, post_id):
  blog = get_object_or_404(BlogPost, pk=post_id)
  comments = Comment.objects.filter(post=blog)
  comment_form = CommentForm()
  return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments, 'comment_form': comment_form})
  likes_post = blog.like_set.filter(liked=True).exists()
  dislikes_post = blog.like_set.filter(liked=False).exists()
  context = {
        'post': post,
        'likes_post': likes_post,
        'dislikes_post': dislikes_post,
    }

def index(request):
  blogs = BlogPost.objects.all()
  return render(request, 'index.html', {'blogs': blogs})

def create_blog(request):
  # pdb.set_trace()            #for debugging 
  if request.method == 'POST':
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('index')
  else:
    form = BlogForm()
  return render(request, 'blog.html', {'form': form})

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

def create_comment(request, post_id):
  blog = get_object_or_404(BlogPost, pk=post_id)
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = blog
      comment.save()
      return redirect('blog_detail', post_id=blog.id)

def edit_comment(request, comment_id):
  comment = get_object_or_404(Comment, pk=comment_id)
  if request.method == 'POST':
    comment_form = CommentForm(request.POST, instance=comment)
    if comment_form.is_valid():
      comment_form.save()
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

@csrf_exempt
def like_unlike_post(request, post_id):
  post = get_object_or_404(BlogPost, pk=post_id)
  dislike, created1 = Like.objects.get_or_create(post=post)
  like, created2 = Like.objects.get_or_create(post=post)
  if request.POST.get('b') == 'lsave':
    if not created2:
      like.liked = True
      like.save()
      dislike.liked = True
      dislike.save()
  elif request.POST.get('b') == 'usave':
    if not created1:
      dislike.liked = False
      dislike.save()
      like.liked = False
      like.save()
  return JsonResponse({'like_count': post.get_like_count(), 'dislike_count': post.get_dislike_count() })
  

