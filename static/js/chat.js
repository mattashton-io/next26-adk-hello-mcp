
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatWindow = document.getElementById('chatWindow');
    const welcomeMessage = document.querySelector('.welcome-message');
    const userId = 'user_' + Math.random().toString(36).substr(2, 9);

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // Clear welcome message on first interaction
        if (welcomeMessage) {
            welcomeMessage.style.display = 'none';
        }

        // Add user message
        addMessage(message, 'user');
        userInput.value = '';

        // Add typing indicator
        const typingId = addTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, message: message })
            });

            const data = await response.json();
            removeTypingIndicator(typingId);

            if (data.error) {
                addMessage('Sorry, I encountered an error: ' + data.error, 'agent', true);
            } else {
                addMessage(data.response, 'agent');
            }
        } catch (error) {
            removeTypingIndicator(typingId);
            addMessage('Failed to connect to the server.', 'agent', true);
            console.error('Error:', error);
        }
    });

    function addMessage(text, role, isError = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}-msg`;
        if (isError) msgDiv.classList.add('error');

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = text;

        msgDiv.appendChild(bubble);
        chatWindow.appendChild(msgDiv);
        scrollToBottom();
    }

    function addTypingIndicator() {
        const id = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message agent-msg typing-indicator';
        typingDiv.id = id;
        
        const bubble = document.createElement('div');
        bubble.className = 'bubble typing';
        bubble.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        
        typingDiv.appendChild(bubble);
        chatWindow.appendChild(typingDiv);
        scrollToBottom();
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});
