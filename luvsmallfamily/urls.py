"""
URL configuration for luvsmallfamily project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# 簡單的首頁視圖 - 重定向到部落格
def home(request):
    from django.shortcuts import redirect
    return redirect('blog:blog_list')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('blog/', include('blog.urls')), # 啟用 blog app 的 URLs
    path('auth/', include('blog.auth_urls')), # 啟用認證功能
    # path('linebot/', include('linebot.urls')),
]

# 開發環境中加入 Debug Toolbar 的 URL 和媒體檔案服務
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    # 在開發環境中提供媒體檔案服務
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
