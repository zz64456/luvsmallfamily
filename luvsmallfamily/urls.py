"""
URL configuration for luvsmallfamily project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import HttpResponse

# 簡單的首頁視圖
def home(request):
    return HttpResponse("歡迎來到 luvsmallfamily 網站！")

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('linebot/', include('linebot.urls')),
]

# 開發環境中加入 Debug Toolbar 的 URL
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
