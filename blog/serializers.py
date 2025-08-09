from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment_date', 'text', 'image_url']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    image_urls = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'created_at', 'comments', 'image_urls']
        
    def get_image_urls(self, obj):
        # This is a placeholder. We will need a way to store multiple images for a post.
        # For now, let's assume we have a way to get them.
        # This part might need to be adjusted based on how we decide to store post images.
        return [
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcToRaWnAZylIpaZZ4UmVojohhW38rjy31i5qQ&s',
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcToRaWnAZylIpaZZ4UmVojohhW38rjy31i5qQ&s',
        ]
