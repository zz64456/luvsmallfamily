# MySQL 8 使用指南

## 🎉 恭喜！您已成功遷移到 MySQL 8

MySQL 8 比 PostgreSQL 更簡單易用，設定也更直接！

## 📋 新的連接資訊

### Navicat 連接設定：
- **主機**: `localhost`
- **端口**: `3306`
- **資料庫**: `mydatabase`
- **用戶名**: `user`
- **密碼**: `password`
- **Root 密碼**: `rootpassword`

## 🚀 快速開始

### 1. 創建 `.env` 文件：

```bash
# Django 設定
SECRET_KEY=dev-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# MySQL 資料庫設定
DATABASE_URL=mysql://user:password@db:3306/mydatabase
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=mydatabase
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_HOST=db
MYSQL_PORT=3306
```

### 2. 啟動開發環境：

```bash
# 清理舊的 PostgreSQL 數據
docker-compose -f docker-compose.dev.yml down -v

# 建立並啟動 MySQL 8 環境
docker-compose -f docker-compose.dev.yml up --build -d

# 等待服務啟動，然後執行遷移
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# 創建超級用戶
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

### 3. 訪問應用：

- **Django 應用**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **MySQL 資料庫**: localhost:3306

## 🔧 MySQL 管理命令

### 進入 MySQL 容器：
```bash
# 進入 MySQL 容器
docker-compose -f docker-compose.dev.yml exec db bash

# 使用 MySQL 客戶端連接
mysql -u user -p mydatabase
# 密碼: password

# 或使用 root 用戶連接
mysql -u root -p
# 密碼: rootpassword
```

### 常用 MySQL 命令：
```sql
-- 查看所有資料庫
SHOW DATABASES;

-- 切換到專案資料庫
USE mydatabase;

-- 查看所有表
SHOW TABLES;

-- 查看表結構
DESCRIBE table_name;

-- 查看 Django 遷移記錄
SELECT * FROM django_migrations;

-- 創建新資料庫（如果需要）
CREATE DATABASE new_database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 🎯 MySQL 8 的優勢

1. **更簡單的設定** - 不需要複雜的 pg_hba.conf 配置
2. **更好的 Windows 支援** - 在 Windows 上運行更穩定
3. **更直觀的管理** - MySQL 工具更容易使用
4. **更好的效能** - 對於大多數 Web 應用效能更好
5. **更豐富的生態系統** - 大量的教程和工具支援

## 📊 資料庫管理工具

### 推薦的 MySQL 管理工具：
- **Navicat for MySQL** - 商業版，功能強大
- **phpMyAdmin** - 免費的 Web 介面
- **MySQL Workbench** - MySQL 官方工具
- **HeidiSQL** - 免費，Windows 專用

## 🔄 備份和恢復

### 備份資料庫：
```bash
# 備份整個資料庫
docker-compose -f docker-compose.dev.yml exec db mysqldump -u user -p mydatabase > backup.sql

# 備份特定表
docker-compose -f docker-compose.dev.yml exec db mysqldump -u user -p mydatabase table_name > table_backup.sql
```

### 恢復資料庫：
```bash
# 恢復資料庫
docker-compose -f docker-compose.dev.yml exec -i db mysql -u user -p mydatabase < backup.sql
```

## 🛠️ 故障排除

### 常見問題：

1. **連接被拒絕**
   - 確認容器正在運行：`docker-compose -f docker-compose.dev.yml ps`
   - 檢查端口是否正確開放

2. **字符集問題**
   - 我們已經設定為 utf8mb4，支援所有 Unicode 字符

3. **權限問題**
   - 檢查用戶名和密碼是否正確
   - 確認用戶有適當的權限

### 查看日誌：
```bash
# 查看 MySQL 日誌
docker-compose -f docker-compose.dev.yml logs db

# 查看 Django 日誌
docker-compose -f docker-compose.dev.yml logs web
```

## 🏭 生產環境部署

生產環境使用相同的 MySQL 8 配置，只需要：

```bash
# 使用生產環境配置
docker-compose up -d --build
```

記得在生產環境中：
1. 設定強密碼
2. 設定 DEBUG=False
3. 配置適當的 ALLOWED_HOSTS
4. 設定 SSL 連接

## 🎊 完成！

您的 Django 項目現在使用 MySQL 8，享受更簡單的開發體驗吧！ 