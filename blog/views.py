from .models import Post, Comment, Media
from .serializers import PostSerializer
from .forms import PostCreateForm, CommentCreateForm
from rest_framework import generics
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.views.generic.edit import FormView
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

        # 先保存 Post 物件
        response = super().form_valid(form)

        # 處理媒體檔案上傳
        self._handle_media_upload(form)
        
        messages.success(self.request, '🎉 文章發布成功！您的愛心故事已經分享給大家了。')
        return response

    def form_invalid(self, form):
        messages.error(self.request, '❌ 發布失敗，請檢查表單內容。')
        return super().form_invalid(form)

    def _handle_media_upload(self, form):
        """處理媒體檔案上傳"""
        post = form.instance
        
        # 處理多張圖片 - 現在可以直接從 cleaned_data 取得
        images = form.cleaned_data.get('images', [])
        for i, image_file in enumerate(images):
            if image_file:  # 確保檔案存在
                Media.objects.create(
                    content_type='post',
                    object_id=post.id,
                    media_type='image',
                    file=image_file,
                    original_filename=image_file.name,
                    file_size=image_file.size,
                    order_index=i
                )
        
        # 處理影片（單個檔案）
        video_file = form.cleaned_data.get('video')
        if video_file:
            Media.objects.create(
                content_type='post',
                object_id=post.id,
                media_type='video',
                file=video_file,
                original_filename=video_file.name,
                file_size=video_file.size,
                order_index=0
            )

# API Views
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')  # 按創建時間降序排序
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# blog/views.py
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['post'] = get_object_or_404(Post, pk=self.kwargs['post_id'])
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        
        response = super().form_valid(form)
        
        # 只有發文者可以上傳媒體
        if self.request.user == post.author:
            self._handle_media_upload(form)
        
        return response
    
    def _handle_media_upload(self, form):
        comment = form.instance
        
        # 處理圖片上傳
        if 'images' in self.request.FILES:
            for i, image_file in enumerate(self.request.FILES.getlist('images')):
                Media.objects.create(
                    content_type='comment',
                    object_id=comment.id,
                    media_type='image',
                    file=image_file,
                    original_filename=image_file.name,
                    file_size=image_file.size,
                    order_index=i
                )
        
        # 處理影片上傳（只能一個）
        if 'video' in self.request.FILES:
            video_file = self.request.FILES['video']
            Media.objects.create(
                content_type='comment',
                object_id=comment.id,
                media_type='video',
                file=video_file,
                original_filename=video_file.name,
                file_size=video_file.size
            )