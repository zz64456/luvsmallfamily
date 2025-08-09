from .models import Post
from .serializers import PostSerializer
from rest_framework import generics
from django.shortcuts import render

# The view for the frontend page, which will consume the API
def blog_page(request):
    return render(request, 'blog/blog_list.html')

# API Views
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer