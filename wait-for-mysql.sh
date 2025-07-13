#!/bin/bash

# 等待 MySQL 準備就緒的腳本

echo "等待 MySQL 數據庫準備就緒..."

# 等待 MySQL 端口可用
while ! nc -z db 3306; do
    echo "MySQL 還未準備就緒，等待中..."
    sleep 2
done

echo "MySQL 端口已開放，測試連接..."

# 使用 Python 測試 MySQL 連接
python << 'EOF'
import pymysql
import time
import sys

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        connection = pymysql.connect(
            host='db',
            user='user',
            password='password',
            database='mydatabase',
            charset='utf8mb4'
        )
        connection.close()
        print("✅ MySQL 連接成功！")
        sys.exit(0)
    except Exception as e:
        retry_count += 1
        print(f"❌ 連接失敗 (嘗試 {retry_count}/{max_retries}): {e}")
        if retry_count < max_retries:
            time.sleep(2)
        else:
            print("❌ 達到最大重試次數，連接失敗！")
            sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo "🚀 啟動 Django 開發伺服器..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "❌ 無法連接到 MySQL，退出..."
    exit 1
fi 