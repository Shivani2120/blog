from django.db import models

# Create your models here.
class BlogPost(models.Model):
  title = models.CharField(max_length=50)
  content = models.CharField(max_length=100)

  def __str__(self):
    return self.title

class Comment(models.Model):
  post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
  author = models.CharField(max_length=50)
  text = models.TextField()
  create_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Comment by {self.author} on {self.post.title}"