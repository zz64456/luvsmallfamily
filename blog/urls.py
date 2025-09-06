from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # URL for the frontend page
    path('', views.blog_page, name='blog_list'),
    
    # 發文功能
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    
    # URLs for the API
    path('api/posts/', views.PostList.as_view(), name='post-list'),
    path('api/posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
]
