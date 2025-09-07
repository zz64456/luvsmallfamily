from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView
from django.http import HttpResponse

from .auth_forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileEditForm
from .tokens import account_activation_token

class LoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('blog:blog_list')

class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('blog:blog_list')

class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('auth:activation_sent')

    def form_valid(self, form):
        user = form.save()
        self.send_activation_email(user)
        return super().form_valid(form)

    def send_activation_email(self, user):
        current_site = get_current_site(self.request)
        mail_subject = '朝日計畫 - 啟用您的帳戶'
        message = render_to_string('auth/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.content_subtype = 'html'
        email.send()

class ActivateAccountView(TemplateView):
    template_name = 'auth/activation_result.html'

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, '恭喜！您的帳戶已成功啟用。')
            return render(request, self.template_name, {'success': True})
        else:
            messages.error(request, '啟用連結無效或已過期。')
            return render(request, self.template_name, {'success': False})

class ActivationSentView(TemplateView):
    template_name = 'auth/activation_sent.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'auth/profile.html'
    login_url = reverse_lazy('auth:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'auth/profile_edit.html'
    success_url = reverse_lazy('auth:profile')
    login_url = reverse_lazy('auth:login')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, '個人資料已成功更新！')
        return super().form_valid(form)

class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'auth/password_change.html'
    success_url = reverse_lazy('auth:password_change_done')
    login_url = reverse_lazy('auth:login')

class PasswordChangeDoneView(LoginRequiredMixin, auth_views.PasswordChangeDoneView):
    template_name = 'auth/password_change_done.html'
    login_url = reverse_lazy('auth:login')
