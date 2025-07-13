# LuvsmallfamilyProject

一個基於 Django 和 Docker 的現代化網站專案，使用 MySQL 8.0 作為資料庫。

## 🚀 專案特色

- **Django 5.2.4** - 現代化的 Python Web 框架
- **MySQL 8.0** - 可靠的關聯式資料庫
- **Docker & Docker Compose** - 容器化部署
- **Redis** - 快取和會話存儲
- **Django Debug Toolbar** - 開發環境調試工具
- **安全配置** - 遵循最佳實踐的安全設定

## 📋 系統需求

- Docker 20.10+
- Docker Compose 1.29+
- Python 3.11+ (本地開發時)

## 🛠️ 快速開始

### 1. 克隆專案

```bash
git clone <your-repo-url>
cd luvsmallfamily
```

### 2. 設置環境變數

```bash
# 複製環境變數範例檔案
cp .env.example .env

# 編輯 .env 文件，填入您的實際配置
# 重要：請勿將 .env 文件提交到版本控制系統！
```

### 3. 環境變數設定

在 `.env` 文件中設定以下變數：

```env
# Django 設定
SECRET_KEY=your-unique-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# 資料庫設定
DATABASE_URL=mysql://user:password@db:3306/mydatabase
MYSQL_ROOT_PASSWORD=your-root-password
MYSQL_DATABASE=your-database-name
MYSQL_USER=your-database-user
MYSQL_PASSWORD=your-database-password
MYSQL_HOST=db
MYSQL_PORT=3306
```

### 4. 啟動開發環境

```bash
# 構建並啟動容器
docker-compose -f docker-compose.dev.yml up --build

# 背景執行
docker-compose -f docker-compose.dev.yml up -d --build
```

### 5. 執行資料庫遷移

```bash
# 創建資料庫表格
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# 創建超級用戶（可選）
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

### 6. 訪問應用程式

- **網站**: http://localhost:8000
- **管理員介面**: http://localhost:8000/admin
- **MySQL 資料庫**: localhost:3306

## 🔧 開發環境

### 查看日誌

```bash
# 查看所有服務日誌
docker-compose -f docker-compose.dev.yml logs -f

# 查看特定服務日誌
docker-compose -f docker-compose.dev.yml logs -f web
```

### 執行 Django 指令

```bash
# 進入容器
docker-compose -f docker-compose.dev.yml exec web bash

# 或直接執行指令
docker-compose -f docker-compose.dev.yml exec web python manage.py shell
```

### 停止服務

```bash
docker-compose -f docker-compose.dev.yml down
```

## 📦 生產環境部署

```bash
# 使用生產環境配置
docker-compose up -d --build

# 收集靜態檔案
docker-compose exec web python manage.py collectstatic --noinput
```

## 🔒 安全性考量

### 環境變數管理

- ✅ 使用 `.env` 文件管理敏感資訊
- ✅ `.env` 文件已加入 `.gitignore`
- ✅ 提供 `.env.example` 範例檔案
- ✅ Docker Compose 使用環境變數而非硬編碼

### 生產環境安全檢查清單

- [ ] 設定強密碼和複雜的 `SECRET_KEY`
- [ ] 將 `DEBUG` 設為 `False`
- [ ] 正確設定 `ALLOWED_HOSTS`
- [ ] 啟用 HTTPS 和安全標頭
- [ ] 定期更新依賴項
- [ ] 使用專用的資料庫用戶

## 🌟 資料庫管理

### 使用 Navicat 連接 MySQL

連接資訊：
- **主機**: localhost
- **端口**: 3306
- **用戶名**: 您在 .env 中設定的 MYSQL_USER
- **密碼**: 您在 .env 中設定的 MYSQL_PASSWORD
- **資料庫**: 您在 .env 中設定的 MYSQL_DATABASE

### 資料庫備份

```bash
# 匯出資料庫
docker-compose -f docker-compose.dev.yml exec db mysqldump -u root -p mydatabase > backup.sql

# 匯入資料庫
docker-compose -f docker-compose.dev.yml exec -i db mysql -u root -p mydatabase < backup.sql
```

## 🤝 貢獻指南

1. Fork 這個專案
2. 創建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟一個 Pull Request

## 📄 許可證

這個專案使用 MIT 許可證。詳情請見 [LICENSE](LICENSE) 文件。

## 📞 聯絡方式

如果您有任何問題或建議，請隨時聯繫：

- 專案連結: [GitHub Repository](https://github.com/yourusername/luvsmallfamily)
- 個人網站: [Your Website](https://yourwebsite.com)

---

⭐ 如果這個專案對您有幫助，請給它一個星星！
