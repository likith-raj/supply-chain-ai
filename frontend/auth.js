const API_BASE = 'https://supply-chain-ai.onrender.com/api';

document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const messageDiv = document.getElementById('message');
    
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store token and user data
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            // Redirect to dashboard
            window.location.href = 'dashboard.html';
        } else {
            messageDiv.innerHTML = `<div style="color: red;">❌ ${data.error}</div>`;
        }
    } catch (error) {
        messageDiv.innerHTML = `<div style="color: red;">❌ Login failed: ${error.message}</div>`;
    }
});

// Check if already logged in
if (localStorage.getItem('token')) {
    window.location.href = 'dashboard.html';
}