from .models import Post
from .serializers import PostSerializer
from .forms import PostCreateForm
from rest_framework import generics
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# The view for the frontend page, which will consume the API
def blog_page(request):
    return render(request, 'blog/blog_list.html')

# 發文功能視圖
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('blog:blog_list')
    login_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        # 設定文章作者為當前登入用戶
        form.instance.author = self.request.user
        messages.success(self.request, '🎉 文章發布成功！您的愛心故事已經分享給大家了。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '❌ 發布失敗，請檢查表單內容。')
        return super().form_invalid(form)

# API Views
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')  # 按創建時間降序排序
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer