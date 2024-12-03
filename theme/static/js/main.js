// User menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const userMenuButton = document.getElementById('user-menu-button');
    const userMenu = document.getElementById('user-menu');
    
    if (userMenuButton && userMenu) {
        userMenuButton.addEventListener('click', function() {
            const expanded = userMenu.classList.contains('hidden');
            userMenu.classList.toggle('hidden');
            userMenuButton.setAttribute('aria-expanded', expanded);
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!userMenuButton.contains(event.target) && !userMenu.contains(event.target)) {
                userMenu.classList.add('hidden');
                userMenuButton.setAttribute('aria-expanded', 'false');
            }
        });
    }
});

// Flash messages auto-dismiss
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Dark mode toggle
document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.documentElement.classList.toggle('dark');
            const isDark = document.documentElement.classList.contains('dark');
            localStorage.setItem('darkMode', isDark ? 'true' : 'false');
        });
    }
});

// WebSocket connection for real-time notifications
class NotificationHandler {
    constructor() {
        this.socket = null;
        this.retryCount = 0;
        this.maxRetries = 5;
        this.retryDelay = 3000;
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const wsUrl = protocol + window.location.host + '/ws/notifications/';
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = () => {
            console.log('WebSocket connected');
            this.retryCount = 0;
        };
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.showNotification(data);
        };
        
        this.socket.onclose = () => {
            console.log('WebSocket disconnected');
            this.retryConnection();
        };
    }

    retryConnection() {
        if (this.retryCount < this.maxRetries) {
            this.retryCount++;
            setTimeout(() => this.connect(), this.retryDelay);
        }
    }

    showNotification(data) {
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-gray-800 text-white px-6 py-4 rounded-lg shadow-lg transform transition-all duration-300 translate-y-0 opacity-100';
        notification.innerHTML = `
            <div class="flex items-center">
                <span class="text-lg">${data.message}</span>
                <button class="ml-4 text-gray-400 hover:text-white" onclick="this.parentElement.parentElement.remove()">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('translate-y-2', 'opacity-0');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
}

// Initialize notification handler if user is authenticated
document.addEventListener('DOMContentLoaded', function() {
    if (document.body.dataset.userAuthenticated === 'true') {
        const notificationHandler = new NotificationHandler();
        notificationHandler.connect();
    }
});
