# Windows 開發環境設置指南

## 前置需求

1. **Docker Desktop for Windows**
   - 下載並安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - 確保 Docker Desktop 正在運行

2. **Git for Windows**
   - 下載並安裝 [Git](https://git-scm.com/download/win)

## 快速開始

### 1. 創建開發環境變量文件

在項目根目錄創建 `.env` 文件：

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

# 開發環境特定設定
DJANGO_SETTINGS_MODULE=luvsmallfamily.settings
```

### 2. 啟動開發環境

在 PowerShell 或 CMD 中執行：

```bash
# 建立並啟動開發環境
docker-compose -f docker-compose.dev.yml up --build

# 如果要在背景執行
docker-compose -f docker-compose.dev.yml up -d --build
```

### 3. 執行資料庫遷移

```bash
# 執行資料庫遷移
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# 創建超級用戶
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

### 4. 訪問應用

- **Django 應用**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **MySQL 資料庫**: localhost:3306 (可用 Navicat 或其他工具連接)
- **Redis**: localhost:6379

## 開發特性

### 1. 熱重載
- 代碼更改會自動重新載入，無需重啟容器
- 靜態文件更改也會自動更新

### 2. Debug Toolbar
- 開發環境自動啟用 Django Debug Toolbar
- 可以查看 SQL 查詢、模板渲染時間等

### 3. Django Extensions
- 提供額外的管理命令
- 如：`python manage.py shell_plus`

### 4. 資料庫存取
- 可以直接從 Windows 連接到 MySQL
- 連接資訊：主機 localhost，端口 3306

## 常用命令

```bash
# 查看容器狀態
docker-compose -f docker-compose.dev.yml ps

# 查看日誌
docker-compose -f docker-compose.dev.yml logs -f

# 進入 Django 容器
docker-compose -f docker-compose.dev.yml exec web bash

# 進入 Django Shell
docker-compose -f docker-compose.dev.yml exec web python manage.py shell

# 重新建置容器
docker-compose -f docker-compose.dev.yml build --no-cache

# 停止所有服務
docker-compose -f docker-compose.dev.yml down

# 停止並刪除數據
docker-compose -f docker-compose.dev.yml down -v
```

## 建議的開發工作流程

1. 啟動開發環境：`docker-compose -f docker-compose.dev.yml up -d`
2. 檢查容器狀態：`docker-compose -f docker-compose.dev.yml ps`
3. 進行開發工作（代碼會自動重載）
4. 執行測試：`docker-compose -f docker-compose.dev.yml exec web python manage.py test`
5. 檢查日誌：`docker-compose -f docker-compose.dev.yml logs -f web`

## 故障排除

### 端口衝突
如果遇到端口衝突，可以修改 `docker-compose.dev.yml` 中的端口映射：
```yaml
ports:
  - "8001:8000"  # 改為其他端口
```

### 權限問題
在 Windows 上，確保 Docker Desktop 有足夠的權限存取專案目錄。

### 容器無法啟動
1. 檢查 Docker Desktop 是否正在運行
2. 檢查防火牆設定
3. 重新建置容器：`docker-compose -f docker-compose.dev.yml build --no-cache`

### MySQL 連接問題
如果遇到 MySQL 連接問題，請參考 `README-MySQL.md` 文件進行故障排除。

### 數據庫連接問題
如果遇到數據庫連接問題：
1. 確保 `.env` 文件中的 MySQL 配置正確
2. 檢查容器是否正常啟動：`docker-compose -f docker-compose.dev.yml ps`
3. 查看 MySQL 日誌：`docker-compose -f docker-compose.dev.yml logs db`

## 生產環境部署

開發完成後，使用原始的 `docker-compose.yml` 進行生產環境部署：

```bash
# 生產環境部署
docker-compose up -d --build
``` 