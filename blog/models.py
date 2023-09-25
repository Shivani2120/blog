from django.db import models

# Create your models here.
class BlogPost(models.Model):
  title = models.CharField(max_length=50)
  content = models.CharField(max_length=100)
  image = models.ImageField(upload_to="images/", null=True, blank=True)
  pdf_file = models.FileField(upload_to='documents/', null=True, blank=True)

  def __str__(self):
    return self.title

  def get_like_count(self):
    return self.like_set.filter(liked=True).count()

  def get_dislike_count(self):
    return self.like_set.filter(liked=False).count()

class Comment(models.Model):
  post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
  author = models.CharField(max_length=50)
  text = models.TextField()
  create_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Comment by {self.author} on {self.post.title}"

class Like(models.Model):
  post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
  liked = models.BooleanField(default=True)