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
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Comment by {self.author} on {self.post.title}"

class Like(models.Model):
  post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
  liked = models.BooleanField(default=True)

# many to many association 
# In this example, an Article can be published in multiple Publication objects, and a Publication has multiple Article objects

class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ["headline"]

    def __str__(self):
        return self.headline

# One to one association 
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.name} the place"


class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name


class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)

##====================== Model Method ======================================##

class Person(models.Model):
  birth_year = models.IntegerField()
  death_year = models.IntegerField(null=True, blank=True)

  def before_hundered(self):
    if (self.birth_year < 100):
      return True
    else:
      return False

  def save(self, *args, **kwargs):
    if (self.birth_year > 100):
      super().save(*args, **kwargs)
    else:
      print("Too Old!")
      return

  def __str__(self):
    return f'%s:%s' % (self.birth_year, self.death_year)