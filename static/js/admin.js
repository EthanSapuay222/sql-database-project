let currentReportId = null;
let newStatus = null;
let pendingChanges = {};

document.addEventListener('DOMContentLoaded', function() {
    loadReports();
});

function loadReports() {
    fetch('/api/admin/reports')
        .then(response => {
            if (response.status === 403) {
                alert('You are not authorized. Please log in as admin.');
                window.location.href = '/user_login';
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.reports) {
                displayReports(data.reports);
                updateStats(data.reports);
            } else if (data && !data.success) {
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
        
        fetch(`/api/admin/reports/${reportId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(changes)
        })
        .then(response => {
            if (response.status === 403) {
                alert('You are not authorized.');
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.success) {
                saveCount++;
                console.log('Report ' + reportId + ' saved');
            } else {
                errorCount++;
                console.error('Error saving report ' + reportId);
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
            console.error('Error:', error);
            if (saveCount + errorCount === totalChanges) {
                pendingChanges = {};
                alert('Saved ' + saveCount + ' reports, but ' + errorCount + ' failed');
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
    
    fetch(`/api/admin/reports/${reportId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.status === 403) {
            alert('You are not authorized.');
            return null;
        }
        return response.json();
    })
    .then(data => {
        if (data && data.success) {
            alert('Report deleted successfully');
            loadReports();
        } else if (data) {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error deleting report:', error);
        alert('Error deleting report: ' + error.message);
    });
}