// Login Page JavaScript

/**
 * Switch between login tabs
 * @param {string} tabName - The ID of the tab to show
 */
function switchTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.add('hidden'));
    tabs.forEach(tab => tab.classList.remove('block'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => {
        btn.classList.remove('border-green-500', 'border-blue-500');
        btn.classList.add('border-transparent');
    });

    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.remove('hidden');
        selectedTab.classList.add('block');
    }

    // Add active class to clicked button
    if (event && event.target) {
        event.target.classList.remove('border-transparent');
        if (tabName === 'admin-login') {
            event.target.classList.add('border-blue-500');
        } else {
            event.target.classList.add('border-green-500');
        }
        event.target.classList.add('active');
    }
}

/**
 * Initialize login page
 */
document.addEventListener('DOMContentLoaded', function() {
    // Handle registration form submission
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegisterSubmit);
    }

    // Add keyboard shortcuts for tab switching
    document.addEventListener('keydown', function(event) {
        // Alt+1: User Login, Alt+2: Register, Alt+3: Admin
        if (event.altKey) {
            switch(event.key) {
                case '1':
                    switchTabByName('user-login');
                    break;
                case '2':
                    switchTabByName('user-register');
                    break;
                case '3':
                    switchTabByName('admin-login');
                    break;
            }
        }
    });
});

/**
 * Handle registration form submission via AJAX
 * @param {Event} event - The form submit event
 */
function handleRegisterSubmit(event) {
    event.preventDefault();

    const registerForm = event.target;
    const formData = new FormData(registerForm);

    // Clear previous error messages
    const errorMessages = document.querySelectorAll('#user-register .mb-4.p-4.bg-red-100');
    errorMessages.forEach(msg => msg.remove());

    // Hide success message initially
    const successMessage = document.getElementById('register-success-message');
    successMessage.classList.add('hidden');

    fetch('/user_register', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message
            successMessage.classList.remove('hidden');
            
            // Clear form
            registerForm.reset();

            // Auto-switch to login tab after 2 seconds
            setTimeout(() => {
                switchTabByName('user-login');
            }, 2000);
        } else {
            // Show error messages
            data.errors.forEach(error => {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded';
                errorDiv.textContent = error;
                registerForm.parentNode.insertBefore(errorDiv, registerForm);
            });
        }
    })
    .catch(error => {
        console.error('Registration error:', error);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded';
        errorDiv.textContent = 'An error occurred during registration. Please try again.';
        registerForm.parentNode.insertBefore(errorDiv, registerForm);
    });
}

/**
 * Switch tab without event parameter
 * @param {string} tabName - The ID of the tab to show
 */
function switchTabByName(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.add('hidden'));
    tabs.forEach(tab => tab.classList.remove('block'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => {
        btn.classList.remove('border-green-500', 'border-blue-500');
        btn.classList.add('border-transparent');
    });

    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.remove('hidden');
        selectedTab.classList.add('block');
    }

    // Update button styling
    buttons.forEach(btn => {
        if (btn.getAttribute('onclick').includes(tabName)) {
            btn.classList.remove('border-transparent');
            if (tabName === 'admin-login') {
                btn.classList.add('border-blue-500');
            } else {
                btn.classList.add('border-green-500');
            }
            btn.classList.add('active');
        }
    });
}
