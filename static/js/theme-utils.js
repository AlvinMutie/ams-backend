// Theme Management - Light Theme Only
function initTheme() {
    // Set light theme as default
    document.documentElement.setAttribute('data-theme', 'light');
}

// Google Translate Integration
function initGoogleTranslate() {
    if (typeof google !== 'undefined' && google.translate) {
        new google.translate.TranslateElement({
            pageLanguage: 'en',
            includedLanguages: 'en,sw,fr,es,ar',
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
            autoDisplay: false
        }, 'google_translate_element');
    }
}

// Language Management
function changeLanguage(lang) {
    localStorage.setItem('language', lang);
    
    // Trigger Google Translate if available
    if (window.google && window.google.translate) {
        const selectElement = document.querySelector('.goog-te-combo');
        if (selectElement) {
            selectElement.value = lang;
            selectElement.dispatchEvent(new Event('change'));
        }
    }
    
    console.log('Language changed to:', lang);
}

function initLanguage() {
    const savedLang = localStorage.getItem('language') || 'en';
    const langSelector = document.querySelector('.language-selector');
    if (langSelector) {
        langSelector.value = savedLang;
    }
}

// Sidebar Management
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    if (sidebar && overlay) {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    }
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    if (sidebar && overlay) {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    }
}

// Notification Management
function toggleNotifications() {
    const notificationPanel = document.getElementById('notificationPanel');
    if (notificationPanel) {
        notificationPanel.classList.toggle('active');
    }
}

// Utility Functions
function addLanguageSelectorToTopBar() {
    const topBarRight = document.querySelector('.top-bar-right');
    if (topBarRight && !document.querySelector('.utility-controls')) {
        const utilityControls = document.createElement('div');
        utilityControls.className = 'utility-controls';
        utilityControls.innerHTML = `
            <div id="google_translate_element"></div>
        `;
        
        // Insert before notification bell
        const notificationBell = topBarRight.querySelector('.notification-bell');
        if (notificationBell) {
            topBarRight.insertBefore(utilityControls, notificationBell);
        } else {
            topBarRight.appendChild(utilityControls);
        }
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initLanguage();
    addLanguageSelectorToTopBar();
    
    // Load Google Translate script
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = '//translate.google.com/translate_a/element.js?cb=initGoogleTranslate';
    document.head.appendChild(script);
});

// Export functions for use in other scripts
window.themeUtils = {
    initTheme,
    changeLanguage,
    initLanguage,
    initGoogleTranslate,
    toggleSidebar,
    closeSidebar,
    toggleNotifications
}; 