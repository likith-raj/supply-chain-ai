const API_BASE = 'http://localhost:5000/api';

async function refreshData() {
    try {
        // Fetch data from backend API
        const [inventoryResponse, deliveriesResponse] = await Promise.all([
            fetch(`${API_BASE}/inventory`),
            fetch(`${API_BASE}/deliveries`)
        ]);

        const inventory = await inventoryResponse.json();
        const deliveries = await deliveriesResponse.json();

        // Update inventory card
        document.getElementById('stock-level').innerHTML = 
            `📦 ${inventory.total_units} units<br>🟢 ${inventory.status}`;

        // Update deliveries card
        document.getElementById('deliveries').innerHTML = 
            `🚚 ${deliveries.active_deliveries} active<br>⏰ ${deliveries.delayed} delayed<br>✅ ${deliveries.on_time} on time`;

        // Show success message
        showNotification('Data updated from server!', 'success');
        
    } catch (error) {
        console.error('Error fetching data:', error);
        showNotification('Failed to connect to server', 'error');
        // Fallback to mock data
        fallbackToMockData();
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