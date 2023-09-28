from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import BlogPost, Comment, Like
from .forms import BlogForm, CommentForm, CreatUserForm
import pdb;
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def blog_detail(request, post_id):
  blog = get_object_or_404(BlogPost, pk=post_id)
  comments = Comment.objects.filter(post=blog)
  comment_form = CommentForm()
  return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments, 'comment_form': comment_form})

@login_required(login_url='login')
def index(request):
  blogs = BlogPost.objects.all()
  return render(request, 'index.html', {'blogs': blogs})

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def delete_blog(request, post_id):
  blog = get_object_or_404(BlogPost, pk=post_id)
  if request.method == 'POST':
    blog.delete()
    messages.success(request,  'The blog has been deleted successfully.')
    return redirect('index')

@login_required(login_url='login')
def create_comment(request, post_id):
  blog = get_object_or_404(BlogPost, pk=post_id)
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = blog
      comment.save()
      return redirect('blog_detail', post_id=blog.id)

@login_required(login_url='login')
def load_comments(request, post_id):
  post = get_object_or_404(BlogPost, id=post_id)
  comments = Comment.objects.filter(post=post.id).order_by('-created_at')[:10] 
  comment_data = [{'id': comment.id, 'text': comment.text, 'created_at': comment.created_at, 'post': comment.post.id, 'author': comment.author} for comment in comments]
  return render(request, 'load_comments.html', {'comments': comment_data})

@login_required(login_url='login')
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

@login_required(login_url='login')
def delete_comment(request, comment_id):
  comment = get_object_or_404(Comment, pk=comment_id)
  if request.method == 'POST':
    post_id = comment.post.id
    comment.delete()
    return redirect('blog_detail', post_id=post_id)

@csrf_exempt 
@login_required(login_url='login')
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

def registrationPage(request):
  if request.user.is_authenticated:
    return redirect('index')
  else:
    form = CreatUserForm()
    if request.method == 'POST':
      form = CreatUserForm(request.POST)
      if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        messages.success(request, "Account was created for " + user)

        return redirect('login')

    context = {'form': form} 
    return render(request, 'register.html', context) 

def loginPage(request):
  if request.user.is_authenticated:
    return redirect('index')
  else:
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)
          messages.info(request, f"You are now logged in as {username}.")
          return redirect("index")
        else:
          messages.error(request,"Invalid username or password.")
          
    context = {}
    return render(request, 'login.html', context) 

@login_required(login_url='login')
def logoutUser(request):
  logout(request)
  messages.info(request, "You have successfully logged out.")
  return redirect('login')
