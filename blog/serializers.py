from rest_framework import serializers
from .models import Post, Comment, Media

class MediaSerializer(serializers.ModelSerializer):
    """媒體檔案序列化器"""
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Media
        fields = ['id', 'media_type', 'file_url', 'original_filename', 'file_size', 'order_index']
    
    def get_file_url(self, obj):
        """返回完整的檔案 URL"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            else:
                return obj.file.url
        return None

class CommentSerializer(serializers.ModelSerializer):
    """留言序列化器"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    is_author_comment = serializers.BooleanField(read_only=True)
    media_files = MediaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id', 'text', 'author_username', 'created_at', 
            'is_author_comment', 'media_files'
        ]

class PostSerializer(serializers.ModelSerializer):
    """文章序列化器"""
    comments = CommentSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    media_files = MediaSerializer(many=True, read_only=True)
    
    # 為了向後兼容，保留 image_urls 欄位
    image_urls = serializers.SerializerMethodField()
    
    # 分別取得圖片和影片
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'text', 'author_username', 'created_at', 
            'comments', 'media_files', 'image_urls', 'images', 'videos'
        ]
        
    def get_image_urls(self, obj):
        """返回所有媒體檔案的 URL（向後兼容）"""
        urls = []
        request = self.context.get('request')
        
        for media in obj.media_files.all():
            if media.file:
                if request:
                    urls.append(request.build_absolute_uri(media.file.url))
                else:
                    urls.append(media.file.url)
        
        return urls
    
    def get_images(self, obj):
        """返回所有圖片的詳細資訊"""
        images = obj.media_files.filter(media_type='image').order_by('order_index')
        return MediaSerializer(images, many=True, context=self.context).data
    
    def get_videos(self, obj):
        """返回所有影片的詳細資訊"""
        videos = obj.media_files.filter(media_type='video').order_by('order_index')
        return MediaSerializer(videos, many=True, context=self.context).data