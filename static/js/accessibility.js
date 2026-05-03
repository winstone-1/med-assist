// Accessibility Features

// Dark Mode Toggle
const darkToggle = document.getElementById('dark-toggle');
if (darkToggle) {
    // Check for saved preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        darkToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
    }
    
    darkToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        if (currentTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            darkToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            darkToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
        }
    });
}

// Font Size Controls
let currentFontSize = 100;
const increaseBtn = document.getElementById('increase-font');
const decreaseBtn = document.getElementById('decrease-font');

if (increaseBtn && decreaseBtn) {
    increaseBtn.addEventListener('click', () => {
        if (currentFontSize < 130) {
            currentFontSize += 10;
            document.body.style.fontSize = currentFontSize + '%';
            localStorage.setItem('fontSize', currentFontSize);
        }
    });
    
    decreaseBtn.addEventListener('click', () => {
        if (currentFontSize > 70) {
            currentFontSize -= 10;
            document.body.style.fontSize = currentFontSize + '%';
            localStorage.setItem('fontSize', currentFontSize);
        }
    });
    
    // Load saved font size
    const savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        currentFontSize = parseInt(savedFontSize);
        document.body.style.fontSize = currentFontSize + '%';
    }
}

// High Contrast Mode
const highContrastBtn = document.getElementById('high-contrast');
if (highContrastBtn) {
    highContrastBtn.addEventListener('click', () => {
        document.body.classList.toggle('high-contrast');
        if (document.body.classList.contains('high-contrast')) {
            localStorage.setItem('highContrast', 'true');
            highContrastBtn.style.backgroundColor = '#ffeb3b';
            highContrastBtn.style.color = '#000';
        } else {
            localStorage.setItem('highContrast', 'false');
            highContrastBtn.style.backgroundColor = '';
            highContrastBtn.style.color = '';
        }
    });
    
    // Load saved high contrast
    if (localStorage.getItem('highContrast') === 'true') {
        document.body.classList.add('high-contrast');
        highContrastBtn.style.backgroundColor = '#ffeb3b';
        highContrastBtn.style.color = '#000';
    }
}

// High Contrast Styles
const highContrastStyle = document.createElement('style');
highContrastStyle.textContent = `
    body.high-contrast {
        filter: contrast(150%) brightness(100%);
    }
    body.high-contrast .card,
    body.high-contrast .feature-card-modern,
    body.high-contrast .testimonial-card {
        border: 2px solid black !important;
    }
    body.high-contrast .btn-teal {
        background: black !important;
        color: white !important;
    }
`;
// Reset all accessibility settings
const resetBtn = document.getElementById('reset-accessibility');

if (resetBtn) {
    resetBtn.addEventListener('click', () => {
        // Reset font size
        currentFontSize = 100;
        document.body.style.fontSize = '100%';
        localStorage.setItem('fontSize', currentFontSize);
        
        // Reset dark mode
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        const darkToggleIcon = document.getElementById('dark-toggle');
        if (darkToggleIcon) darkToggleIcon.innerHTML = '<i class="fa-solid fa-moon"></i> Dark';
        
        // Reset high contrast
        document.body.classList.remove('high-contrast');
        localStorage.setItem('highContrast', 'false');
        const highContrastBtn = document.getElementById('high-contrast');
        if (highContrastBtn) {
            highContrastBtn.style.backgroundColor = '';
            highContrastBtn.style.color = '';
        }
        
        // Show success message
        alert('All accessibility settings have been reset to default.');
    });
}
document.head.appendChild(highContrastStyle);