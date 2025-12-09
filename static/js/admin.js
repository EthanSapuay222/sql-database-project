let currentReportId = null;
let newStatus = null;
let pendingChanges = {};

console.log('Admin.js loaded - checking session...');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - attempting to fetch reports');
    loadReports();
});

function loadReports() {
    fetch('/api/admin/reports', {
        credentials: 'include'
    })
        .then(response => {
            console.log('Response status:', response.status);
            if (response.status === 403) {
                console.error('Unauthorized - redirecting to login');
                alert('You are not authorized. Please log in as admin.');
                window.location.href = '/admin/login';
                return null;
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Reports data:', data);
            if (!data) return;
            if (data.reports) {
                displayReports(data.reports);
                updateStats(data.reports);
            } else if (!data.success) {
                console.error('Error:', data.message);
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error loading reports:', error);
            alert('Error loading reports: ' + error.message);
        });
}

function updateStats(reports) {
    let pending = 0;
    let completed = 0;
    
    reports.forEach(report => {
        if (report.status === 'pending') pending++;
        else if (report.status === 'completed') completed++;
    });
    
    document.getElementById('total-reports').textContent = reports.length;
    document.getElementById('pending-reports').textContent = pending;
    document.getElementById('approved-reports').textContent = completed;
}

function displayReports(reports) {
    const tbody = document.getElementById('reports-tbody');
    
    if (reports.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">No reports submitted yet</td></tr>';
        return;
    }
    
    tbody.innerHTML = reports.map(report => `
        <tr id="report-row-${report.report_id}">
            <td>#${report.report_id}</td>
            <td>${report.title}</td>
            <td>${report.report_type}</td>
            <td>${report.severity}</td>
            <td><span id="status-${report.report_id}" class="status-badge ${report.status}">${report.status.replace('_', ' ').toUpperCase()}</span></td>
            <td>${report.reporter_name || 'N/A'}</td>
            <td>
                <div id="actions-${report.report_id}" class="action-buttons">
                    ${getStatusButtons(report.report_id, report.status)}
                    <button class="delete" onclick="deleteReport(${report.report_id})">Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
}

function getStatusButtons(reportId, status) {
    const statusOrder = ['pending', 'in_progress', 'completed'];
    const currentIndex = statusOrder.indexOf(status);
    const nextStatus = statusOrder[(currentIndex + 1) % statusOrder.length];
    const statusLabel = nextStatus.replace('_', ' ').toUpperCase();
    
    return `<button onclick="changeStatus(${reportId}, '${nextStatus}')" class="status-btn">${statusLabel}</button>`;
}

function changeStatus(reportId, newStatus) {
    // Store the change without saving immediately
    if (!pendingChanges[reportId]) {
        pendingChanges[reportId] = {};
    }
    pendingChanges[reportId].status = newStatus;
    
    // Update status badge live
    const statusElement = document.getElementById(`status-${reportId}`);
    statusElement.textContent = newStatus.replace('_', ' ').toUpperCase();
    statusElement.className = `status-badge ${newStatus}`;
    
    // Update buttons live
    const actionsDiv = document.getElementById(`actions-${reportId}`);
    const deleteButton = actionsDiv.querySelector('.delete');
    actionsDiv.innerHTML = getStatusButtons(reportId, newStatus);
    actionsDiv.appendChild(deleteButton);
}

function saveAllChanges() {
    if (Object.keys(pendingChanges).length === 0) {
        alert('No changes to save');
        return;
    }
    
    let saveCount = 0;
    let errorCount = 0;
    const totalChanges = Object.keys(pendingChanges).length;
    
    // Save all pending changes
    Object.keys(pendingChanges).forEach(reportId => {
        const changes = pendingChanges[reportId];
        console.log(`Sending changes for report ${reportId}:`, changes);
        
        fetch(`/api/admin/reports/${reportId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(changes)
        })
        .then(response => {
            console.log(`PUT response for report ${reportId}:`, response.status);
            if (response.status === 403) {
                console.error('Unauthorized for report ' + reportId);
                errorCount++;
                if (saveCount + errorCount === totalChanges) {
                    pendingChanges = {};
                    alert('You are not authorized to edit reports');
                    loadReports();
                    updateSummaryStats();
                }
                return null;
            }
            return response.json().then(data => {
                if (!response.ok) {
                    console.error(`Server error for report ${reportId}:`, data);
                    throw new Error(data.message || `HTTP error! status: ${response.status}`);
                }
                return data;
            });
        })
        .then(data => {
            if (!data) return; // Handle 403 case
            console.log(`Save response for report ${reportId}:`, data);
            if (data && data.success) {
                saveCount++;
                console.log('Report ' + reportId + ' saved');
            } else if (data) {
                errorCount++;
                console.error('Error saving report ' + reportId + ':', data.message);
            }
            
            // If all changes processed, clear and reload
            if (saveCount + errorCount === totalChanges) {
                pendingChanges = {};
                if (errorCount === 0) {
                    showSuccessMessage('Saved successfully!');
                    loadReports();
                    updateSummaryStats();
                } else {
                    alert('Saved ' + saveCount + ' reports, but ' + errorCount + ' failed');
                    loadReports();
                    updateSummaryStats();
                }
            }
        })
        .catch(error => {
            errorCount++;
            console.error('Fetch error for report ' + reportId + ':', error);
            if (saveCount + errorCount === totalChanges) {
                pendingChanges = {};
                alert('Saved ' + saveCount + ' reports, but ' + errorCount + ' failed\n\nError: ' + error.message);
                loadReports();
                updateSummaryStats();
            }
        });
    });
}

function showSuccessMessage(message) {
    // Create success message element
    const successDiv = document.createElement('div');
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #28a745;
        color: white;
        padding: 15px 20px;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        z-index: 10000;
        font-size: 16px;
        font-weight: 600;
    `;
    successDiv.textContent = message;
    
    document.body.appendChild(successDiv);
    
    // Remove after 3 seconds
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

function updateSummaryStats() {
    // Count reports by status from the table
    const rows = document.querySelectorAll('#reports-tbody tr');
    let pending = 0;
    let completed = 0;
    
    rows.forEach(row => {
        const statusSpan = row.querySelector('[class*="status-badge"]');
        if (statusSpan) {
            const status = statusSpan.textContent.toLowerCase().replace(' ', '_');
            if (status === 'pending') pending++;
            else if (status === 'completed') completed++;
        }
    });
    
    document.getElementById('total-reports').textContent = rows.length;
    document.getElementById('pending-reports').textContent = pending;
    document.getElementById('approved-reports').textContent = completed;
}


function deleteReport(reportId) {
    if (!confirm('Are you sure you want to delete this report?')) {
        return;
    }
    
    console.log('Deleting report:', reportId);
    fetch(`/api/admin/reports/${reportId}`, {
        method: 'DELETE',
        credentials: 'include'
    })
    .then(response => {
        console.log('Delete response status:', response.status);
        if (!response.ok) {
            if (response.status === 403) {
                throw new Error('You are not authorized to delete reports.');
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Delete response data:', data);
        if (data.success) {
            alert('Report deleted successfully');
            loadReports();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error deleting report:', error);
        alert('Error deleting report: ' + error.message);
    });
}

// Tab switching functionality
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
        tab.classList.add('hidden');
    });
    
    // Deactivate all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    const tabElement = document.getElementById(tabName + '-tab');
    if (tabElement) {
        tabElement.classList.add('active');
        tabElement.classList.remove('hidden');
    }
    
    // Activate clicked button
    event.target.classList.add('active');
    
    // Load data for the tab
    if (tabName === 'sightings') {
        loadSightings();
    } else if (tabName === 'users') {
        loadUsers();
    }
}

// Load animal sightings
function loadSightings() {
    fetch('/api/admin/sightings', {
        credentials: 'include'
    })
        .then(response => {
            if (response.status === 403) {
                alert('You are not authorized.');
                window.location.href = '/admin/login';
                return null;
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;
            if (data.success && data.data) {
                displaySightings(data.data);
                updateSightingStats(data.data);
            } else {
                console.error('Error:', data.message);
            }
        })
        .catch(error => {
            console.error('Error loading sightings:', error);
            alert('Error loading sightings: ' + error.message);
        });
}

function displaySightings(sightings) {
    const tbody = document.getElementById('sightings-tbody');
    
    if (!sightings || sightings.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">No sightings submitted yet</td></tr>';
        return;
    }
    
    tbody.innerHTML = sightings.map(sighting => `
        <tr>
            <td>${sighting.sighting_id}</td>
            <td>${sighting.species?.common_name || 'Unknown'}</td>
            <td>${sighting.location?.city_name || 'Unknown'}</td>
            <td>${sighting.observer_name || 'N/A'}</td>
            <td>${new Date(sighting.sighting_date).toLocaleDateString()}</td>
            <td>${sighting.verification_status || 'pending'}</td>
            <td>
                <button class="delete-btn" onclick="deleteSighting(${sighting.sighting_id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function updateSightingStats(sightings) {
    let pending = 0;
    let verified = 0;
    
    sightings.forEach(sighting => {
        if (sighting.verification_status === 'verified') {
            verified++;
        } else if (sighting.verification_status === 'pending') {
            pending++;
        }
    });
    
    document.getElementById('total-sightings').textContent = sightings.length;
    document.getElementById('pending-sightings').textContent = pending;
    document.getElementById('verified-sightings').textContent = verified;
}

function deleteSighting(sightingId) {
    if (!confirm('Are you sure you want to delete this sighting?')) {
        return;
    }
    
    fetch(`/api/admin/sightings/${sightingId}`, {
        method: 'DELETE',
        credentials: 'include'
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Sighting deleted successfully');
                loadSightings();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error deleting sighting:', error);
            alert('Error deleting sighting: ' + error.message);
        });
}

// Load users
function loadUsers() {
    fetch('/api/admin/users', {
        credentials: 'include'
    })
        .then(response => {
            if (response.status === 403) {
                alert('You are not authorized.');
                window.location.href = '/admin/login';
                return null;
            }
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;
            if (data.success && data.data) {
                displayUsers(data.data);
                updateUserStats(data.data);
            } else {
                console.error('Error:', data.message);
            }
        })
        .catch(error => {
            console.error('Error loading users:', error);
            alert('Error loading users: ' + error.message);
        });
}

function displayUsers(users) {
    const tbody = document.getElementById('users-tbody');
    
    if (!users || users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No users found</td></tr>';
        return;
    }
    
    tbody.innerHTML = users.map(user => `
        <tr>
            <td>${user.user_id}</td>
            <td>${user.username}</td>
            <td>${user.email || 'N/A'}</td>
            <td>${user.role || 'user'}</td>
            <td>${new Date(user.created_at).toLocaleDateString()}</td>
            <td>
                <button class="delete-btn" onclick="deleteUser(${user.user_id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function updateUserStats(users) {
    document.getElementById('total-users').textContent = users.length;
}

function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
        return;
    }
    
    fetch(`/api/admin/users/${userId}`, {
        method: 'DELETE',
        credentials: 'include'
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('User deleted successfully');
                loadUsers();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error deleting user:', error);
            alert('Error deleting user: ' + error.message);
        });
}
