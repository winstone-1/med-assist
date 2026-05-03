// Chatbot AI Responses
const chatbotResponses = {
    // Symptom related
    'chest pain': 'Chest pain can be serious. If you have crushing chest pain, pain radiating to arm/jaw, or shortness of breath, call emergency services (999/112) immediately.',
    'fever': 'For fever over 38°C (100.4°F), rest, stay hydrated, and take paracetamol. Seek medical attention if fever lasts more than 3 days or exceeds 40°C (104°F).',
    'headache': 'For mild headaches, rest and hydrate. See a doctor if you have sudden severe headache, headache with fever, or after head injury.',
    'cough': 'For cough, rest and drink warm fluids. Seek care if you have difficulty breathing, cough up blood, or have cough lasting more than 3 weeks.',
    
    // First aid related
    'choking': 'For choking: 1) Ask if person is choking 2) Call 999/112 3) Give 5 back blows 4) Give 5 abdominal thrusts (Heimlich) 5) Repeat until object is cleared.',
    'burns': 'For burns: 1) Cool under running water for 20 minutes 2) Remove jewellery 3) Cover with sterile dressing. Do NOT apply ice or butter.',
    'bleeding': 'For severe bleeding: 1) Call emergency services 2) Apply firm direct pressure 3) Raise injured limb 4) Keep pressure until help arrives.',
    'fracture': 'For suspected fracture: 1) Do not move person 2) Immobilize area 3) Apply ice pack wrapped in cloth 4) Seek medical attention.',
    
    // Conditions
    'cold symptoms': 'Common cold symptoms include: runny nose, sore throat, cough, sneezing, mild fever, and fatigue. Most colds resolve within 7-10 days.',
    'flu symptoms': 'Flu symptoms include: sudden high fever, body aches, headache, extreme fatigue, dry cough, and sore throat. Rest and hydrate.',
    'allergy symptoms': 'Allergy symptoms include: sneezing, runny/blocked nose, itchy/watery eyes, rash. Antihistamines can help.',
    
    // Emergency
    'when to go to er': 'Go to ER for: chest pain, difficulty breathing, severe bleeding, head injury with confusion, sudden severe headache, paralysis, or loss of consciousness.',
    'emergency signs': 'Emergency signs include: difficulty breathing, chest pain, severe bleeding, sudden confusion, inability to wake up, or severe allergic reaction.',
    
    // General health
    'blood pressure': 'Normal BP is below 120/80. High BP is 130/90 or above. Consult your doctor for personalized advice.',
    'bmi': 'BMI categories: Underweight (<18.5), Normal (18.5-24.9), Overweight (25-29.9), Obese (30+). BMI is a screening tool, not diagnostic.',
    'hydration': 'Adults should drink 2-3 liters of water daily. Signs of dehydration: dark urine, dry mouth, fatigue, dizziness.',
    'sleep': 'Adults need 7-9 hours of sleep per night. Good sleep hygiene: consistent schedule, dark room, no screens before bed.',
    
    // Default
    'default': "I'm here to help! You can ask me about symptoms, first aid, conditions, or when to seek emergency care. What would you like to know?"
};

// Main chat function
function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage(message, 'user');
    input.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Get AI response after delay
    setTimeout(() => {
        removeTypingIndicator();
        const response = getAIResponse(message);
        addMessage(response, 'bot');
        
        // Update notification badge
        const notification = document.getElementById('chatNotification');
        if (notification && !document.getElementById('chatbotContainer').classList.contains('open')) {
            const count = parseInt(notification.textContent) || 0;
            notification.textContent = count + 1;
        }
    }, 500 + Math.random() * 500);
}

function getAIResponse(userMessage) {
    const lowerMessage = userMessage.toLowerCase();
    
    // Check for keywords
    for (const [keyword, response] of Object.entries(chatbotResponses)) {
        if (lowerMessage.includes(keyword)) {
            return response;
        }
    }
    
    // Check for question patterns
    if (lowerMessage.includes('how long') || lowerMessage.includes('duration')) {
        return 'Symptom duration matters. Acute symptoms (<7 days) are often viral. Chronic symptoms (>2 weeks) may need medical evaluation.';
    }
    
    if (lowerMessage.includes('should i see a doctor')) {
        return 'See a doctor if: symptoms are severe, lasting >7 days, worsening, or if you have high fever, difficulty breathing, or chest pain.';
    }
    
    if (lowerMessage.includes('thank')) {
        return "You're welcome! Stay healthy and consult a doctor for medical advice. Is there anything else I can help with?";
    }
    
    if (lowerMessage.includes('hi') || lowerMessage.includes('hello')) {
        return "Hello! I'm MedAssist AI. Ask me about symptoms, first aid, medications, or health concerns.";
    }
    
    return "I understand you're asking about: " + userMessage + "\n\nFor accurate medical advice, please consult a healthcare professional. Would you like to check symptoms using our symptom checker instead?";
}

function addMessage(text, sender) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const now = new Date();
    const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fa-solid ${sender === 'bot' ? 'fa-robot' : 'fa-user'}"></i>
        </div>
        <div class="message-content">
            <div class="message-text">${escapeHtml(text)}</div>
            <div class="message-time">${timeString}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/\n/g, '<br>');
}

function showTypingIndicator() {
    const messagesDiv = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot typing-indicator-container';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fa-solid fa-robot"></i>
        </div>
        <div class="typing-indicator">
            <span></span><span></span><span></span>
        </div>
    `;
    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('chatSend');
    const chatInput = document.getElementById('chatInput');
    const chatToggle = document.getElementById('chatbotToggle');
    const chatContainer = document.getElementById('chatbotContainer');
    const chatClose = document.querySelector('.chatbot-close');
    const chatMinimize = document.getElementById('chatMinimize');
    const quickReplies = document.querySelectorAll('.quick-reply');
    
    if (sendBtn) sendBtn.addEventListener('click', sendMessage);
    if (chatInput) chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    if (chatToggle) {
        chatToggle.addEventListener('click', () => {
            chatContainer.classList.toggle('open');
            if (chatContainer.classList.contains('open')) {
                document.getElementById('chatNotification').style.display = 'none';
                document.getElementById('chatNotification').textContent = '0';
            }
        });
    }
    
    if (chatClose) {
        chatClose.addEventListener('click', () => {
            chatContainer.classList.remove('open');
        });
    }
    
    if (chatMinimize) {
        chatMinimize.addEventListener('click', () => {
            chatContainer.classList.remove('open');
        });
    }
    
    quickReplies.forEach(reply => {
        reply.addEventListener('click', () => {
            const question = reply.getAttribute('data-question');
            document.getElementById('chatInput').value = question;
            sendMessage();
        });
    });
    
    // Close chat when clicking outside
    document.addEventListener('click', (e) => {
        if (chatContainer && !chatContainer.contains(e.target) && !chatToggle.contains(e.target)) {
            chatContainer.classList.remove('open');
        }
    });
});