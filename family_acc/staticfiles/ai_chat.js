document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('ai-chat-container');
    const toggleButton = document.getElementById('ai-chat-toggle');
    const closeButton = document.getElementById('close-chat');
    const sendButton = document.getElementById('send-ai-message');
    const userInput = document.getElementById('ai-user-input');
    const chatHistory = document.getElementById('ai-chat-history');

    // Toggle Chat Visibility
    toggleButton.addEventListener('click', () => {
        chatContainer.classList.remove('ai-chat-hidden');
        toggleButton.classList.add('ai-chat-hidden');
    });

    closeButton.addEventListener('click', () => {
        chatContainer.classList.add('ai-chat-hidden');
        toggleButton.classList.remove('ai-chat-hidden');
    });

    // Handle Sending Messages
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage('user', message);
        userInput.value = '';

        // Fetch CSRF token from cookies
        const csrftoken = getCookie('csrftoken');

        // Send to your Django backend (Update this URL to your actual view path)
        fetch('/ai/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('ai', data.reply);
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('ai', 'Sorry, I encountered an error. Please try again.');
        });
    }

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message`;
        msgDiv.textContent = text;
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    // Standard Django function to get CSRF token from cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    if (window.visualViewport) {
        window.visualViewport.addEventListener('resize', updateButtonPosition);
        window.visualViewport.addEventListener('scroll', updateButtonPosition);
    }

    function updateButtonPosition() {
        const vv = window.visualViewport;
        const toggleButton = document.getElementById('ai-chat-toggle');
        const chatContainer = document.getElementById('ai-chat-container');
        const offset = 20; // Your desired margin from the edge

        // window.innerHeight/Width represent the Layout Viewport
        const layoutHeight = window.innerHeight;
        const layoutWidth = window.innerWidth;

        /**
         * Correct Calculation for position: fixed:
         * We calculate the distance between the bottom/right of the 
         * Layout Viewport and the bottom/right of the Visual Viewport.
         */
        const bottom = layoutHeight - (vv.offsetTop + vv.height) + offset;
        const right = layoutWidth - (vv.offsetLeft + vv.width) + offset;

        if (toggleButton) {
            toggleButton.style.bottom = `${bottom}px`;
            toggleButton.style.right = `${right}px`;
            
            /**
             * Optional: Scaling Correction
             * Browsers automatically scale 'fixed' elements during zoom. 
             * This keeps the button at a consistent physical size.
             */
            toggleButton.style.transform = `scale(${1 / vv.scale})`;
            toggleButton.style.transformOrigin = 'bottom right';
        }

        if (chatContainer && !chatContainer.classList.contains('ai-chat-hidden')) {
            chatContainer.style.bottom = `${bottom}px`;
            chatContainer.style.right = `${right}px`;
            chatContainer.style.transform = `scale(${1 / vv.scale})`;
            chatContainer.style.transformOrigin = 'bottom right';
        }
    }
});