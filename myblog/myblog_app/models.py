from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length=200)
  author = models.ForeignKey('auth.user', on_delete=models.CASCADE)
  body = models.TextField()
  
  def __str__(self):
      return self.title
    
  def get_absolute_url(self):
    return reverse('post_detail', args=[str(self.id)])
  
  
# class Comment(models.Model):
#   post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name ='comments')
#   user = models.ForeignKey(User, on_delete = models.CASCADE)
#   content = models.TextField()
  
class Comment(models.Model):
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
   name = models.CharField(max_length=80) 
   email = models.EmailField() 
   body = models.TextField() 
   created = models.DateTimeField(auto_now_add=True) 
   updated = models.DateTimeField(auto_now=True) 
   active = models.BooleanField(default=False) 
   slug = models.SlugField(blank=True, editable=False)

class Meta: 
  ordering = ('created') 

  def __str__(self): 
      return 'Comment by {} on {}'.format(self.name, self.post) 
  