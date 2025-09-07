from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': '請輸入您的電子郵件'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '請輸入您的姓名'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '請輸入用戶名（字母、數字、@/./+/-/_）'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '請輸入密碼（至少8個字符）'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '請再次輸入密碼確認'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("此電子郵件已被註冊")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.is_active = False  # 需要郵件驗證才能啟用
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '用戶名或電子郵件'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '密碼'
        })

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '姓名'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '姓氏（可選）'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': '電子郵件'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("此電子郵件已被使用")
        return email
