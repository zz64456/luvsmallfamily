/**
 * 朝日計畫 - 主要JavaScript功能
 * 包含：部落格功能、手機菜單、圖片輪播、留言區
 */

document.addEventListener('DOMContentLoaded', function () {
    // 初始化所有功能
    initMobileMenu();
    loadBlogPosts();
});

/**
 * 手機菜單功能
 */
function initMobileMenu() {
    const menuToggle = document.getElementById('menu-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
        
        // 點擊導航連結時關閉手機菜單
        navMenu.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                navMenu.classList.remove('active');
            }
        });
    }
}

/**
 * 載入部落格文章
 */
function loadBlogPosts() {
    const postContainer = document.getElementById('post-container');
    if (!postContainer) return;

    fetch('/blog/api/posts/')
        .then(response => response.json())
        .then(posts => {
            posts.forEach((post, index) => {
                const postElement = document.createElement('div');
                postElement.className = 'post';
                postElement.innerHTML = createPostHTML(post, index + 1);
                postContainer.appendChild(postElement);
            });
            
            // 延遲初始化以確保DOM已渲染
            setTimeout(initializePageLogic, 0);
        })
        .catch(error => {
            console.error('載入文章時發生錯誤:', error);
            postContainer.innerHTML = '<p style="text-align: center; color: #666;">載入文章時發生錯誤，請稍後再試。</p>';
        });
}

/**
 * 創建文章HTML
 */
function createPostHTML(post, postIndex) {
    const swiperHTML = createSwiperHTML(post.image_urls, postIndex);
    const commentsHTML = createCommentsHTML(post.comments);

    return `
        <div class="post-media" data-post-id="${post.id}">
            ${swiperHTML}
        </div>
        <div class="post-content">
            <p>${post.text}</p>
            <div class="comment-section">
                <h3>留言區</h3>
                <div class="accordion">${commentsHTML}</div>
            </div>
        </div>
    `;
}

/**
 * 創建圖片輪播HTML
 */
function createSwiperHTML(mediaUrls, postIndex) {
    if (mediaUrls.length > 1) {
        const slides = mediaUrls.map(url => {
            // 判斷是圖片還是影片
            if (isVideoUrl(url)) {
                return `<div class="swiper-slide">
                    <video controls class="swiper-video">
                        <source src="${url}" type="video/mp4">
                        您的瀏覽器不支援影片播放。
                    </video>
                </div>`;
            } else {
                return `<div class="swiper-slide">
                    <img src="${url}" alt="部落格圖片" class="swiper-image clickable-image" onclick="openLightbox('${url}')">
                </div>`;
            }
        }).join('');
        
        return `
            <div id="swiper-container-${postIndex}" class="swiper-container">
                <div class="swiper-wrapper">${slides}</div>
                <div class="swiper-pagination swiper-pagination-${postIndex}"></div>
                <div class="swiper-button-next swiper-button-next-${postIndex}"></div>
                <div class="swiper-button-prev swiper-button-prev-${postIndex}"></div>
            </div>`;
    } else if (mediaUrls.length === 1) {
        const url = mediaUrls[0];
        if (isVideoUrl(url)) {
            return `
                <div class="swiper-container single-media">
                    <div class="swiper-slide">
                        <video controls class="swiper-video">
                            <source src="${url}" type="video/mp4">
                            您的瀏覽器不支援影片播放。
                        </video>
                    </div>
                </div>`;
        } else {
            return `
                <div class="swiper-container single-media">
                    <div class="swiper-slide">
                        <img src="${url}" alt="部落格圖片" class="swiper-image clickable-image" onclick="openLightbox('${url}')">
                    </div>
                </div>`;
        }
    }
    return '';
}

/**
 * 判斷 URL 是否為影片
 * @param {string} url - 媒體文件 URL
 * @returns {boolean} 是否為影片
 */
function isVideoUrl(url) {
    const videoExtensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv'];
    const urlLower = url.toLowerCase();
    return videoExtensions.some(ext => urlLower.includes(ext)) || urlLower.includes('/videos/');
}

/**
 * 創建留言區HTML
 */
function createCommentsHTML(comments) {
    return comments.map(comment => `
        <div class="accordion-item">
            <button class="accordion-header">${new Date(comment.comment_date).toLocaleDateString('en-CA')} 留言</button>
            <div class="accordion-content">
                ${comment.comment_type === 'text' ? `<p>${comment.text}</p>` : ''}
                ${comment.comment_type === 'image' ? `<img src="${comment.image_url}" class="comment-image" alt="留言圖片">` : ''}
            </div>
        </div>
    `).join('');
}

/**
 * 初始化頁面邏輯（輪播、手風琴、燈箱）
 */
function initializePageLogic() {
    initializeSwipers();
    initializeAccordions();
    initializeImageLightbox();
}

/**
 * 初始化Swiper輪播
 */
function initializeSwipers() {
    document.querySelectorAll('.post').forEach((post, index) => {
        const container = post.querySelector('.swiper-container:not(.single-image)');
        if (container) {
            new Swiper(`#swiper-container-${index + 1}`, {
                observer: true,
                observeParents: true,
                slidesPerView: 1, 
                spaceBetween: 10, 
                loop: true, 
                grabCursor: true,
                pagination: { 
                    el: `.swiper-pagination-${index + 1}`, 
                    clickable: true 
                },
                navigation: { 
                    nextEl: `.swiper-button-next-${index + 1}`, 
                    prevEl: `.swiper-button-prev-${index + 1}` 
                },
            });
        }
    });
}

/**
 * 初始化手風琴功能
 */
function initializeAccordions() {
    document.querySelectorAll('.accordion').forEach(accordion => {
        const items = accordion.querySelectorAll('.accordion-item');
        
        items.forEach(item => {
            item.querySelector('.accordion-header').addEventListener('click', () => {
                toggleAccordionItem(accordion, item);
            });
        });

        // 預設打開第一個（最新的）留言
        openFirstAccordionItem(items);
    });
}

/**
 * 切換手風琴項目
 */
function toggleAccordionItem(accordion, item) {
    const currentlyActive = accordion.querySelector('.accordion-item.active');
    
    if (currentlyActive && currentlyActive !== item) {
        currentlyActive.classList.remove('active');
        currentlyActive.querySelector('.accordion-content').style.maxHeight = null;
    }
    
    item.classList.toggle('active');
    const content = item.querySelector('.accordion-content');
    content.style.maxHeight = content.style.maxHeight ? null : content.scrollHeight + "px";
}

/**
 * 打開第一個手風琴項目
 */
function openFirstAccordionItem(items) {
    const firstItem = items[0];
    if (firstItem) {
        firstItem.classList.add('active');
        const content = firstItem.querySelector('.accordion-content');
        
        // 使用小延遲確保瀏覽器已渲染元素
        setTimeout(() => {
            content.style.maxHeight = content.scrollHeight + "px";
        }, 100);
    }
}

/**
 * 打開圖片燈箱
 * @param {string} imageUrl - 圖片 URL
 */
function openLightbox(imageUrl) {
    const lightbox = document.getElementById('image-lightbox');
    const lightboxImage = lightbox?.querySelector('img');
    
    if (!lightbox || !lightboxImage) {
        console.error('燈箱元素未找到');
        return;
    }
    
    lightboxImage.src = imageUrl;
    lightbox.style.display = 'flex';
}

/**
 * 初始化圖片燈箱功能
 */
function initializeImageLightbox() {
    const lightbox = document.getElementById('image-lightbox');
    const lightboxImage = lightbox?.querySelector('img');
    
    if (!lightbox || !lightboxImage) return;

    // 為留言圖片添加點擊事件
    document.querySelectorAll('.comment-image').forEach(image => {
        image.addEventListener('click', () => {
            lightboxImage.src = image.src;
            lightbox.style.display = 'flex';
        });
    });

    // 點擊燈箱關閉
    lightbox.addEventListener('click', () => {
        lightbox.style.display = 'none';
    });
}
