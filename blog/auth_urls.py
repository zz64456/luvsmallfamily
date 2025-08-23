from django.urls import path
from . import auth_views

app_name = 'auth'

urlpatterns = [
    # 登入/登出
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # 註冊相關
    path('register/', auth_views.RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', auth_views.ActivateAccountView.as_view(), name='activate'),
    path('activation-sent/', auth_views.ActivationSentView.as_view(), name='activation_sent'),
    
    # 用戶資料
    path('profile/', auth_views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', auth_views.ProfileEditView.as_view(), name='profile_edit'),
    
    # 密碼相關
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
