# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.author.username}"
    
    @property
    def media_files(self):
        """取得文章的所有媒體檔案"""
        return Media.objects.filter(content_type='post', object_id=self.pk)
    
    @property
    def images(self):
        """取得文章的所有圖片"""
        return self.media_files.filter(media_type='image')
    
    @property
    def videos(self):
        """取得文章的所有影片"""
        return self.media_files.filter(media_type='video')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # 留言按時間正序

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    @property
    def is_author_comment(self):
        """檢查是否為發文者的留言"""
        return self.author == self.post.author
    
    @property
    def can_upload_media(self):
        """檢查是否可以上傳媒體（只有發文者可以）"""
        return self.is_author_comment
    
    @property
    def media_files(self):
        """取得留言的所有媒體檔案"""
        return Media.objects.filter(content_type='comment', object_id=self.pk)
    
    @property
    def images(self):
        """取得留言的所有圖片"""
        return self.media_files.filter(media_type='image')
    
    @property
    def videos(self):
        """取得留言的所有影片"""
        return self.media_files.filter(media_type='video')

class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    CONTENT_TYPE_CHOICES = [
        ('post', 'Post'),
        ('comment', 'Comment'),
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    object_id = models.BigIntegerField()
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='media/%Y/%m/')
    original_filename = models.CharField(max_length=255, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_index', 'created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['media_type']),
        ]

    def __str__(self):
        return f"{self.media_type} for {self.content_type} #{self.object_id}"
    
    @property
    def is_image(self):
        return self.media_type == 'image'
    
    @property
    def is_video(self):
        return self.media_type == 'video'