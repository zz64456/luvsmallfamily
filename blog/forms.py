from django import forms
from .models import Post, Comment

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            result = [super(MultipleFileField, self).clean(d, initial) for d in data]
        else:
            result = [super(MultipleFileField, self).clean(data, initial)]
        return result

class PostCreateForm(forms.ModelForm):
    # 添加媒體上傳欄位（不是模型欄位）
    images = MultipleFileField(
        required=False,
        help_text='支援 JPG, PNG, GIF 格式，可選擇多張圖片，單張最大 10MB'
    )
    
    video = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'video/*',
            'class': 'form-file-input'
        }),
        help_text='支援 MP4, AVI, MOV 格式，最大 50MB'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'text']  # 只包含 Post 模型的實際欄位
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '請輸入文章標題',
                'required': True
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': '分享您的故事，幫助更多流浪動物找到溫暖的家...',
                'rows': 8,
                'required': True
            }),
        }
        labels = {
            'title': '文章標題',
            'text': '文章內容',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 設定必填欄位
        self.fields['title'].required = True
        self.fields['text'].required = True

    def clean_images(self):
        """驗證圖片檔案"""
        images = self.files.getlist('images')
        if not isinstance(images, list):
            images = [images] if images else []

        for image in images:
            if image.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError(f'圖片 {image.name} 檔案大小不能超過 10MB')
        return images

    def clean_video(self):
        """驗證影片檔案"""
        video = self.cleaned_data.get('video')
        if video:
            if video.size > 50 * 1024 * 1024:  # 50MB
                raise forms.ValidationError('影片檔案大小不能超過 50MB')
        return video

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': '分享您的想法...',
                'rows': 3
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # 只有發文者可以看到媒體上傳欄位
        if self.user and self.post and self.user == self.post.author:
            self.fields['images'] = MultipleFileField(
                required=False,
                help_text='發文者可以上傳多張圖片'
            )
            self.fields['video'] = forms.FileField(
                required=False,
                widget=forms.FileInput(attrs={
                    'accept': 'video/*',
                    'class': 'form-file-input'
                }),
                help_text='發文者可以上傳一個影片'
            )
