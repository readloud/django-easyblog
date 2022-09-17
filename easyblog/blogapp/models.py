from django.db import models

# Create your models here.
from django.db import models
class BlogModel(models.Model):
    id = models.IntegerField(primary_key=True)
    blog_title = models.CharField(max_length=20)
    blog = models.TextField()
 
    def __str__(self):
        return f"Blog: {self.blog_title}"
 
class CommentModel(models.Model):
    your_name = models.CharField(max_length=20)
    comment_text = models.TextField()
    blog = models.ForeignKey('BlogModel', on_delete=models.CASCADE)
     
    def __str__(self):
        return f"Comment by Name: {self.your_name}"