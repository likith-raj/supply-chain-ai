function refreshData() {
    document.getElementById('stock-level').innerHTML = 
        '📦 1,245 units<br>🟢 Good Stock';
    
    document.getElementById('deliveries').innerHTML = 
        '🚚 15 active deliveries<br>⏰ 2 delayed<br>✅ 13 on time';
    
    alert('Data Updated Successfully!');
}

// Load initial data when page opens
refreshData();