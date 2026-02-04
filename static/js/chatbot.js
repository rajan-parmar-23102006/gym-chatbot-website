// Chatbot functionality
document.addEventListener('DOMContentLoaded', function() {
    
    // Get elements
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatbotClose = document.getElementById('chatbot-close');
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatbotMessages = document.getElementById('chatbot-messages');
    
    // Toggle chatbot visibility
    chatbotToggle.addEventListener('click', function() {
        chatbotContainer.classList.toggle('active');
        if (chatbotContainer.classList.contains('active')) {
            userInput.focus();
        }
    });
    
    // Close chatbot
    chatbotClose.addEventListener('click', function() {
        chatbotContainer.classList.remove('active');
    });
    
    // Send message on button click
    sendBtn.addEventListener('click', function() {
        sendMessage();
    });
    
    // Send message on Enter key
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Function to send message
    function sendMessage() {
        const message = userInput.value.trim();
        
        if (message === '') {
            return;
        }
        
        // Display user message
        addMessage(message, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send to backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            removeTypingIndicator();
            
            if (data.status === 'success') {
                // Display bot response
                addMessage(data.response, 'bot');
            } else {
                addMessage('Sorry, something went wrong. Please try again.', 'bot');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage('Sorry, I am having trouble connecting. Please try again later.', 'bot');
        });
    }
    
    // Function to add message to chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
        
        const messageText = document.createElement('p');
        
        // Convert markdown-style bold (**text**) to HTML
        const formattedText = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
        
        messageText.innerHTML = formattedText;
        messageDiv.appendChild(messageText);
        
        chatbotMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'bot-message typing-indicator';
        typingDiv.id = 'typing-indicator';
        
        const typingText = document.createElement('p');
        typingText.innerHTML = '<em>Typing...</em>';
        typingDiv.appendChild(typingText);
        
        chatbotMessages.appendChild(typingDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                // Close mobile menu if open
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                }
            }
        });
    });
    
    // Add active state to navbar on scroll
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.8)';
        } else {
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.5)';
        }
    });
    
});