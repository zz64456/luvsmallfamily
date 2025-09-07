# 朝日計畫 - 靜態文件架構

## 📁 文件結構

```
blog/static/blog/
├── css/
│   ├── variables.css    # CSS變量定義（色彩、間距等）
│   ├── base.css        # 基礎樣式和重置
│   ├── header.css      # Header導航樣式
│   ├── hero.css        # Hero section樣式
│   ├── blog.css        # 部落格內容樣式
│   └── main.css        # 主要CSS文件（導入所有模組）
└── js/
    └── main.js         # 主要JavaScript功能
```

## 🎨 CSS模組化設計

### variables.css
- 定義所有顏色變量（warm-orange主題）
- 統一間距、圓角、陰影等設計token
- 便於全局主題調整

### base.css
- CSS重置和基礎樣式
- 通用按鈕樣式
- 響應式基礎設定

### header.css
- 頂部導航樣式
- Logo和菜單設計
- 手機響應式菜單

### hero.css
- 主要展示區塊樣式
- 統計數據網格
- 漸變背景和動畫

### blog.css
- 文章卡片樣式
- Swiper輪播定制
- 留言區手風琴效果
- 圖片燈箱樣式

## 🚀 JavaScript模組化

### main.js
- 模組化函數結構
- 錯誤處理
- 性能優化
- 清晰的註釋和文檔

## 📱 響應式設計

所有CSS文件都包含完整的響應式設計：
- 桌面版（>768px）
- 平板版（640px-768px）
- 手機版（<640px）

## 🔧 使用方式

在Django模板中載入：

```html
{% load static %}
<link rel="stylesheet" href="{% static 'blog/css/main.css' %}">
<script src="{% static 'blog/js/main.js' %}"></script>
```

## 🎯 優點

1. **維護性**：模組化結構便於維護和更新
2. **可讀性**：清晰的文件組織和命名
3. **重用性**：CSS變量和模組可在其他頁面重用
4. **效能**：減少HTML文件大小，更好的快取策略
5. **擴展性**：為未來的SCSS和現代工具鏈做好準備

## 🔄 升級路徑

這個架構為未來升級做好了準備：
- **階段2**：將CSS轉換為SCSS
- **階段3**：引入Vite等現代工具鏈
- **階段4**：添加TypeScript支援
