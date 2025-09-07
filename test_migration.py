#!/usr/bin/env python
"""
測試 migration 的腳本
使用方法：python test_migration.py
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luvsmallfamily.settings')
django.setup()

from django.db import connection
from blog.models import Post, Comment, Media

def check_migration_status():
    """檢查 migration 狀態"""
    print("🔍 檢查 migration 狀態...")
    
    with connection.cursor() as cursor:
        # 檢查是否存在舊的欄位
        cursor.execute("SHOW COLUMNS FROM blog_post LIKE 'image'")
        has_old_image = cursor.fetchone() is not None
        
        cursor.execute("SHOW COLUMNS FROM blog_post LIKE 'video'")
        has_old_video = cursor.fetchone() is not None
        
        # 檢查是否存在新的 Media 表
        cursor.execute("SHOW TABLES LIKE 'blog_media'")
        has_media_table = cursor.fetchone() is not None
    
    print(f"📊 Migration 狀態:")
    print(f"  - Post 表有舊的 image 欄位: {'是' if has_old_image else '否'}")
    print(f"  - Post 表有舊的 video 欄位: {'是' if has_old_video else '否'}")
    print(f"  - 存在新的 Media 表: {'是' if has_media_table else '否'}")
    
    return has_old_image, has_old_video, has_media_table

def test_data_integrity():
    """測試資料完整性"""
    print("\n🧪 測試資料完整性...")
    
    try:
        # 測試 Post 查詢
        posts = Post.objects.all()
        print(f"  - 文章總數: {posts.count()}")
        
        # 測試 Media 查詢
        media_files = Media.objects.all()
        print(f"  - 媒體檔案總數: {media_files.count()}")
        
        # 測試關聯查詢
        for post in posts[:3]:  # 只測試前3篇文章
            images = post.images
            videos = post.videos
            print(f"  - 文章 '{post.title}': {images.count()} 張圖片, {videos.count()} 個影片")
        
        # 測試 Comment 查詢
        comments = Comment.objects.all()
        print(f"  - 留言總數: {comments.count()}")
        
        print("✅ 資料完整性測試通過！")
        return True
        
    except Exception as e:
        print(f"❌ 資料完整性測試失敗: {e}")
        return False

def main():
    print("🚀 開始測試 Migration...")
    print("=" * 50)
    
    # 檢查 migration 狀態
    has_old_image, has_old_video, has_media_table = check_migration_status()
    
    if has_old_image or has_old_video:
        print("\n⚠️  發現舊的媒體欄位，建議執行 migration:")
        print("   python manage.py migrate blog 0004")
        return
    
    if not has_media_table:
        print("\n❌ 未找到 Media 表，請先執行 migration:")
        print("   python manage.py migrate blog 0004")
        return
    
    # 測試資料完整性
    if test_data_integrity():
        print("\n🎉 Migration 測試完成！所有功能正常。")
    else:
        print("\n⚠️  發現問題，請檢查 migration 邏輯。")

if __name__ == '__main__':
    main()
