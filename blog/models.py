from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # 按創建時間降序排序

    def __str__(self):
        return f"{self.title} - {self.author.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment_date = models.DateField()
    comment_type = models.CharField(max_length=10, choices=[('text', 'Text'), ('image', 'Image')], default='text')
    text = models.CharField(max_length=200, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return f'Comment by on {self.post.title} at {self.comment_date}'