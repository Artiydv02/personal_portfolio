document.addEventListener('DOMContentLoaded', function() {
    // Animation for section elements
    const animateElements = document.querySelectorAll('.animate-fadeIn');
    animateElements.forEach(element => {
        element.classList.add('animate-fadeIn');
    });
    
    // Initialize Typed.js if element exists
    if (document.querySelector('.typed-text')) {
        new Typed('.typed-text', {
            strings: [
                "Business Analyst",
                "Data Enthusiast",
                "Python Developer",
                "Problem Solver"
            ],
            typeSpeed: 80,
            backSpeed: 40,
            backDelay: 2000,
            loop: true
        });
    }
    
    // Chat functionality
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const questionSuggestions = document.querySelectorAll('.question-suggestion');
    
    // If chat elements exist
    if (chatForm && chatInput && chatMessages) {
        // Handle form submission
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const message = chatInput.value.trim();
            if (message !== '') {
                // Add user message to chat
                addMessage(message, 'user');
                
                // Clear input
                chatInput.value = '';
                
                // Get bot response
                getBotResponse(message);
            }
        });
        
        // Handle question suggestions
        if (questionSuggestions) {
            questionSuggestions.forEach(suggestion => {
                suggestion.addEventListener('click', function() {
                    const question = this.textContent;
                    
                    // Add user message to chat
                    addMessage(question, 'user');
                    
                    // Get bot response
                    getBotResponse(question);
                });
            });
        }
    }
    
    // Function to add message to chat
    function addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        
        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        contentElement.textContent = message;
        
        messageElement.appendChild(contentElement);
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to get bot response from server
    function getBotResponse(message) {
        // Create a "thinking" message
        const thinkingElement = document.createElement('div');
        thinkingElement.classList.add('message', 'bot', 'thinking');
        
        const contentElement = document.createElement('div');
        contentElement.classList.add('message-content');
        contentElement.textContent = 'Thinking...';
        
        thinkingElement.appendChild(contentElement);
        chatMessages.appendChild(thinkingElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Send request to server
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove thinking message
            chatMessages.removeChild(thinkingElement);
            
            // Add bot response
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            // Remove thinking message
            chatMessages.removeChild(thinkingElement);
            
            // Add error message
            addMessage('Sorry, I encountered an error. Please try again later.', 'bot');
            console.error('Error:', error);
        });
    }
    
    // Scroll animations
    const elements = document.querySelectorAll('.scroll-animate');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeIn');
                
                // Animate skill progress bars if they exist in this section
                const skillBars = entry.target.querySelectorAll('.skill-progress');
                if (skillBars.length > 0) {
                    setTimeout(() => {
                        skillBars.forEach(bar => {
                            const width = bar.getAttribute('data-width');
                            bar.style.width = width;
                        });
                    }, 300);
                }
                
                // Animate timeline items if they exist in this section
                const timelineItems = entry.target.querySelectorAll('.timeline-item');
                if (timelineItems.length > 0) {
                    timelineItems.forEach((item, index) => {
                        setTimeout(() => {
                            item.classList.add('animate');
                        }, 300 * (index + 1)); // Staggered animation
                    });
                }
            }
        });
    }, { threshold: 0.1 });
    
    elements.forEach(element => {
        observer.observe(element);
    });
    
    // Initialize skill bars when page loads
    const initSkillBars = () => {
        const skillItems = document.querySelectorAll('.skill-item');
        if (skillItems.length > 0) {
            skillItems.forEach(item => {
                const progressBar = item.querySelector('.skill-progress');
                if (progressBar) {
                    progressBar.style.width = '0%';
                }
            });
        }
    };
    
    initSkillBars();
    
    // PDF Zoom functionality
    const zoomIn = document.getElementById('zoom-in');
    const zoomOut = document.getElementById('zoom-out');
    const pdfViewer = document.querySelector('.pdf-viewer');
    
    if (zoomIn && zoomOut && pdfViewer) {
        let currentScale = 1.0;
        const scaleStep = 0.1;
        const minScale = 0.5;
        const maxScale = 2.0;
        
        zoomIn.addEventListener('click', () => {
            if (currentScale < maxScale) {
                currentScale += scaleStep;
                pdfViewer.style.transform = `scale(${currentScale})`;
                pdfViewer.style.transformOrigin = 'center top';
            }
        });
        
        zoomOut.addEventListener('click', () => {
            if (currentScale > minScale) {
                currentScale -= scaleStep;
                pdfViewer.style.transform = `scale(${currentScale})`;
                pdfViewer.style.transformOrigin = 'center top';
            }
        });
    }
});