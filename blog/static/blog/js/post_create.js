/**
 * 發文頁面 JavaScript 功能
 * 包含：多圖片上傳、影片上傳、預覽、拖拽功能
 */

// 存儲選中的圖片文件
let selectedImages = [];
let selectedVideo = null;

document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('id_images');
    const videoInput = document.getElementById('id_video');
    const imagePreviewGrid = document.getElementById('image-preview-grid');
    const videoPreviewGrid = document.getElementById('video-preview-grid');
    
    // 多圖片選擇和預覽
    imageInput.addEventListener('change', function(e) {
        const files = Array.from(e.target.files);
        
        if (files.length > 0) {
            // 不再清除影片選擇，允許同時上傳
            
            // 添加新選中的圖片
            files.forEach(file => {
                if (file.size > 10 * 1024 * 1024) {
                    alert(`圖片 ${file.name} 超過 10MB 限制`);
                    return;
                }
                
                selectedImages.push(file);
                addImagePreview(file);
            });
            
            updateImageInput();
        }
    });
    
    // 影片選擇和預覽
    videoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        
        if (file) {
            if (file.size > 50 * 1024 * 1024) {
                alert('影片檔案超過 50MB 限制');
                videoInput.value = '';
                return;
            }
            
            // 不再清除圖片選擇，允許同時上傳
            
            selectedVideo = file;
            addVideoPreview(file);
        }
    });
    
    // 初始化拖拽功能
    initializeDragAndDrop();
    
    // 初始化表單驗證
    initializeFormValidation();
});

/**
 * 添加圖片預覽
 * @param {File} file - 圖片文件
 */
function addImagePreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewItem = document.createElement('div');
        previewItem.className = 'preview-item';
        previewItem.innerHTML = `
            <img src="${e.target.result}" alt="圖片預覽" class="preview-image">
            <div class="file-info">${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</div>
            <button type="button" class="remove-btn" onclick="removeImage('${file.name}')" title="移除圖片">
                ✕
            </button>
        `;
        document.getElementById('image-preview-grid').appendChild(previewItem);
    };
    reader.readAsDataURL(file);
}

/**
 * 添加影片預覽
 * @param {File} file - 影片文件
 */
function addVideoPreview(file) {
    const videoUrl = URL.createObjectURL(file);
    const previewItem = document.createElement('div');
    previewItem.className = 'preview-item';
    previewItem.innerHTML = `
        <video src="${videoUrl}" class="preview-video" controls></video>
        <div class="file-info">${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</div>
        <button type="button" class="remove-btn" onclick="removeVideo()" title="移除影片">
            ✕
        </button>
    `;
    document.getElementById('video-preview-grid').appendChild(previewItem);
}

/**
 * 移除指定圖片
 * @param {string} fileName - 要移除的圖片文件名
 */
function removeImage(fileName) {
    selectedImages = selectedImages.filter(file => file.name !== fileName);
    updateImageInput();
    renderImagePreviews();
}

/**
 * 移除影片
 */
function removeVideo() {
    selectedVideo = null;
    document.getElementById('id_video').value = '';
    document.getElementById('video-preview-grid').innerHTML = '';
}

/**
 * 清除所有圖片
 */
function clearImages() {
    selectedImages = [];
    document.getElementById('id_images').value = '';
    document.getElementById('image-preview-grid').innerHTML = '';
}

/**
 * 清除影片
 */
function clearVideo() {
    selectedVideo = null;
    document.getElementById('id_video').value = '';
    document.getElementById('video-preview-grid').innerHTML = '';
}

/**
 * 更新隱藏的圖片輸入框
 */
function updateImageInput() {
    const dt = new DataTransfer();
    selectedImages.forEach(file => dt.items.add(file));
    document.getElementById('id_images').files = dt.files;
}

/**
 * 重新渲染圖片預覽
 */
function renderImagePreviews() {
    const grid = document.getElementById('image-preview-grid');
    grid.innerHTML = '';
    selectedImages.forEach(file => addImagePreview(file));
}

/**
 * 初始化拖拽上傳功能
 */
function initializeDragAndDrop() {
    const uploadSection = document.querySelector('.upload-section');
    
    uploadSection.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadSection.style.borderColor = 'hsl(var(--warm-orange))';
        uploadSection.style.backgroundColor = 'rgba(255,255,255,0.9)';
    });
    
    uploadSection.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadSection.style.borderColor = 'hsl(var(--warm-orange) / 0.3)';
        uploadSection.style.backgroundColor = '';
    });
    
    uploadSection.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadSection.style.borderColor = 'hsl(var(--warm-orange) / 0.3)';
        uploadSection.style.backgroundColor = '';
        
        const files = Array.from(e.dataTransfer.files);
        const imageFiles = files.filter(file => file.type.startsWith('image/'));
        const videoFiles = files.filter(file => file.type.startsWith('video/'));
        
        if (imageFiles.length > 0) {
            // 不清除影片，允許同時上傳
            imageFiles.forEach(file => {
                if (file.size <= 10 * 1024 * 1024) {
                    selectedImages.push(file);
                    addImagePreview(file);
                } else {
                    alert(`圖片 ${file.name} 超過 10MB 限制`);
                }
            });
            updateImageInput();
        }
        
        if (videoFiles.length > 0) {
            const videoFile = videoFiles[0];
            if (videoFile.size <= 50 * 1024 * 1024) {
                // 不清除圖片，允許同時上傳
                selectedVideo = videoFile;
                
                // 手動設置影片輸入框
                const dt = new DataTransfer();
                dt.items.add(videoFile);
                document.getElementById('id_video').files = dt.files;
                
                addVideoPreview(videoFile);
            } else {
                alert('影片檔案超過 50MB 限制');
            }
        }
    });
}

/**
 * 初始化表單驗證
 */
function initializeFormValidation() {
    document.getElementById('post-form').addEventListener('submit', function(e) {
        const title = document.querySelector('#id_title').value.trim();
        const text = document.querySelector('#id_text').value.trim();
        
        if (!title || !text) {
            e.preventDefault();
            alert('請填寫標題和內容！');
            return false;
        }

        // 允許同時上傳圖片和影片
        
        // 顯示提交中的狀態
        const submitBtn = document.querySelector('button[type="submit"]');
        submitBtn.innerHTML = '📤 發布中...';
        submitBtn.disabled = true;
        
        // 模型支持單張圖片，如果選擇多張則使用第一張
        if (selectedImages.length > 1) {
            console.log('選擇了多張圖片，將使用第一張');
        }
    });
}

/**
 * 文件大小格式化
 * @param {number} bytes - 文件大小（字節）
 * @returns {string} 格式化後的文件大小
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * 檢查文件類型是否支持
 * @param {File} file - 要檢查的文件
 * @param {string} type - 文件類型 ('image' 或 'video')
 * @returns {boolean} 是否支持
 */
function isFileTypeSupported(file, type) {
    if (type === 'image') {
        return file.type.startsWith('image/') && 
               ['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(file.type);
    } else if (type === 'video') {
        return file.type.startsWith('video/') && 
               ['video/mp4', 'video/avi', 'video/mov', 'video/quicktime'].includes(file.type);
    }
    return false;
}
