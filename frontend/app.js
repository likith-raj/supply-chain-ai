const API_BASE = 'https://supply-chain-ai.onrender.com/api';

async function makeAuthenticatedRequest(url) {
    const token = localStorage.getItem('token');
    
    const response = await fetch(url, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    
    if (response.status === 401) {
        // Token expired or invalid
        logout();
        throw new Error('Authentication failed');
    }
    
    return response;
}

async function refreshData() {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = 'index.html';
            return;
        }

        // Fetch data from backend API with authentication
        const [inventoryResponse, deliveriesResponse] = await Promise.all([
            makeAuthenticatedRequest(`${API_BASE}/inventory`),
            makeAuthenticatedRequest(`${API_BASE}/deliveries`)
        ]);

        const inventory = await inventoryResponse.json();
        const deliveries = await deliveriesResponse.json();

        // Update inventory card
        document.getElementById('stock-level').innerHTML = 
            `📦 ${inventory.total_units} units<br>🟢 ${inventory.status}`;
        
        document.getElementById('company-info').textContent = 
            `Company: ${inventory.user_company}`;

        // Update deliveries card
        document.getElementById('deliveries').innerHTML = 
            `🚚 ${deliveries.active_deliveries} active<br>⏰ ${deliveries.delayed} delayed<br>✅ ${deliveries.on_time} on time`;
        
        document.getElementById('delivery-info').textContent = 
            `Managed by: ${deliveries.user_company}`;

        showNotification('✅ Data updated successfully!', 'success');
        
    } catch (error) {
        console.error('Error fetching data:', error);
        if (error.message === 'Authentication failed') {
            showNotification('🔐 Please login again', 'error');
        } else {
            showNotification('❌ Failed to fetch data', 'error');
            fallbackToMockData();
        }
    }
}

function fallbackToMockData() {
    document.getElementById('stock-level').innerHTML = 
        '📦 1,245 units<br>🟢 Good Stock';
    document.getElementById('deliveries').innerHTML = 
        '🚚 15 active<br>⏰ 2 delayed<br>✅ 13 on time';
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px;
        background: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        border-radius: 5px;
        z-index: 1000;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Load initial data when page loads
document.addEventListener('DOMContentLoaded', function() {
    refreshData();
});