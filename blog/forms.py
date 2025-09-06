from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'video']
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
            'image': forms.FileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/*',
                'id': 'image-upload'
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-file-input',
                'accept': 'video/*',
                'id': 'video-upload'
            })
        }
        labels = {
            'title': '文章標題',
            'text': '文章內容',
            'image': '上傳圖片',
            'video': '上傳影片'
        }
        help_texts = {
            'image': '支援 JPG, PNG, GIF 格式，最大 10MB',
            'video': '支援 MP4, AVI, MOV 格式，最大 50MB'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 設定必填和選填欄位
        self.fields['title'].required = True
        self.fields['text'].required = True
        self.fields['image'].required = False
        self.fields['video'].required = False

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError('圖片檔案大小不能超過 10MB')
        return image

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if video.size > 50 * 1024 * 1024:  # 50MB
                raise forms.ValidationError('影片檔案大小不能超過 50MB')
        return video

    # def clean(self):
    #     cleaned_data = super().clean()
        
    #     return cleaned_data
