# Generated manually for media model restructure

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


def migrate_post_media_to_media_table(apps, schema_editor):
    """將現有的 Post 媒體檔案遷移到新的 Media 表"""
    Post = apps.get_model('blog', 'Post')
    Media = apps.get_model('blog', 'Media')
    
    for post in Post.objects.all():
        # 遷移圖片
        if post.image:
            Media.objects.create(
                content_type='post',
                object_id=post.id,
                media_type='image',
                file=post.image.name,  # 只保存檔案路徑
                original_filename=post.image.name.split('/')[-1],
                order_index=0,
            )
        
        # 遷移影片
        if post.video:
            Media.objects.create(
                content_type='post',
                object_id=post.id,
                media_type='video',
                file=post.video.name,  # 只保存檔案路徑
                original_filename=post.video.name.split('/')[-1],
                order_index=1,
            )


def reverse_migrate_media_to_post(apps, schema_editor):
    """反向遷移：將 Media 資料還原到 Post 表（用於 migration 回滾）"""
    Post = apps.get_model('blog', 'Post')
    Media = apps.get_model('blog', 'Media')
    
    for post in Post.objects.all():
        # 還原第一張圖片
        first_image = Media.objects.filter(
            content_type='post',
            object_id=post.id,
            media_type='image'
        ).first()
        if first_image:
            post.image = first_image.file
        
        # 還原第一個影片
        first_video = Media.objects.filter(
            content_type='post',
            object_id=post.id,
            media_type='video'
        ).first()
        if first_video:
            post.video = first_video.file
        
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_options_post_author_post_image_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # 1. 創建新的 Media 模型
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('post', 'Post'), ('comment', 'Comment')], max_length=20)),
                ('object_id', models.BigIntegerField()),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], max_length=10)),
                ('file', models.FileField(upload_to='media/%Y/%m/')),
                ('original_filename', models.CharField(blank=True, max_length=255)),
                ('file_size', models.BigIntegerField(blank=True, null=True)),
                ('order_index', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['order_index', 'created_at'],
            },
        ),
        
        # 2. 添加資料庫索引
        migrations.AddIndex(
            model_name='media',
            index=models.Index(fields=['content_type', 'object_id'], name='blog_media_content_type_object_id_idx'),
        ),
        migrations.AddIndex(
            model_name='media',
            index=models.Index(fields=['media_type'], name='blog_media_media_type_idx'),
        ),
        
        # 3. 修改 Comment 模型 - 添加 author 欄位
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        
        # 4. 修改 Comment 的 text 欄位為 TextField
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(),
        ),
        
        # 5. 修改 Comment 的排序
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at']},
        ),
        
        # 6. 遷移現有的媒體資料
        migrations.RunPython(
            migrate_post_media_to_media_table,
            reverse_migrate_media_to_post,
        ),
        
        # 7. 移除 Post 模型中的舊媒體欄位
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.RemoveField(
            model_name='post',
            name='video',
        ),
        
        # 8. 移除 Comment 模型中的舊欄位
        migrations.RemoveField(
            model_name='comment',
            name='comment_date',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='comment_type',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='image_url',
        ),
    ]
