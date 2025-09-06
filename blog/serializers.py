from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment_date', 'comment_type', 'text', 'image_url']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    image_urls = serializers.SerializerMethodField()
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'author_username', 'created_at', 'comments', 'image_urls']
        
    def get_image_urls(self, obj):
        """返回文章的實際圖片和影片 URL"""
        urls = []
        
        # 如果有圖片，添加圖片 URL
        if obj.image:
            # 構建完整的圖片 URL
            request = self.context.get('request')
            if request:
                urls.append(request.build_absolute_uri(obj.image.url))
            else:
                urls.append(obj.image.url)
        
        # 如果有影片，添加影片 URL
        if obj.video:
            request = self.context.get('request')
            if request:
                urls.append(request.build_absolute_uri(obj.video.url))
            else:
                urls.append(obj.video.url)
        
        # 如果沒有任何媒體文件，返回空列表
        return urls
