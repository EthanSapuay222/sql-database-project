// Dashboard Charts and Initialization

document.addEventListener('DOMContentLoaded', function() {
  // Update status display
  const userIdDisplay = document.getElementById("user-id-display");
  if (userIdDisplay) {
    userIdDisplay.innerHTML = `<span class="font-bold">Status:</span> Dashboard Ready`;
  }

  // Load all dashboard data
  loadCategoryDistribution();
  loadSightingsByLocation('land');
  loadSightingsByLocation('water');
  loadReports();
  loadAnimalSightings();
  loadDashboardStats();
});

// Category Distribution Chart - Report Types
async function loadCategoryDistribution() {
  try {
    const response = await fetch('/api/dashboard/reports-by-type');
    const result = await response.json();

    const pieCtx = document.getElementById("categoryDistributionChart");
    if (!pieCtx || !result.success || !result.data.length) {
      console.log('No category data available');
      return;
    }

    const colors = {
      'pollution': '#ef4444',
      'habitat_loss': '#f59e0b',
      'illegal_activity': '#8b5cf6',
      'wildlife_incident': '#10b981',
      'other': '#6b7280'
    };

    const labels = result.data.map(item => {
      const name = item.type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      return `${name}: ${item.count}`;
    });
    const data = result.data.map(item => item.count);
    const backgroundColors = result.data.map(item => colors[item.type] || '#6dd9e8');

    new Chart(pieCtx.getContext("2d"), {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: backgroundColors,
          hoverOffset: 16,
          borderWidth: 2,
          borderColor: "#ffffff",
        }],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              color: "#374151",
              font: { size: 12 },
            },
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                return context.label;
              },
            },
          },
        },
      },
    });
  } catch (error) {
    console.error('Error loading category distribution:', error);
  }
}

// Load Sightings by Location (Land or Water)
async function loadSightingsByLocation(category) {
  try {
    const response = await fetch(`/api/dashboard/sightings-by-location?category=${category}&limit=5`);
    const result = await response.json();

    const chartId = category === 'land' ? 'landSightingsChart' : 'waterSightingsChart';
    const ctx = document.getElementById(chartId);
    
    if (!ctx) return;

    const labels = result.data && result.data.length > 0 
      ? result.data.map(item => item.city) 
      : ['No data'];
    const data = result.data && result.data.length > 0 
      ? result.data.map(item => item.sightings) 
      : [0];
    const maxValue = Math.max(...data, 10);

    const accentColor = category === 'land' ? '#6d824d' : '#6dd9e8';
    const accentColorDark = category === 'land' ? '#556938' : '#3aa4b0';

    new Chart(ctx.getContext("2d"), {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Sightings",
          data: data,
          backgroundColor: accentColor,
          borderColor: accentColorDark,
          borderWidth: 1,
          borderRadius: 6,
          barPercentage: 0.7,
        }],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            suggestedMax: maxValue + 2,
            grid: { color: "rgba(200, 200, 200, 0.2)" },
            ticks: { stepSize: 1 }
          },
          x: {
            grid: { display: false },
          },
        },
        plugins: {
          legend: { display: false },
          title: { display: false },
        },
      },
    });
  } catch (error) {
    console.error(`Error loading ${category} sightings:`, error);
  }
}

// Load Dashboard Stats
async function loadDashboardStats() {
  try {
    const response = await fetch('/api/dashboard/stats');
    const result = await response.json();

    if (result.success && result.data) {
      const stats = result.data;
      
      // Update stat cards
      const statCards = document.querySelectorAll('.grid.grid-cols-2 .p-4');
      if (statCards.length >= 4) {
        statCards[0].querySelector('.text-3xl').textContent = stats.total_reports || 0;
        statCards[1].querySelector('.text-3xl').textContent = stats.pending_reports || 0;
        statCards[2].querySelector('.text-3xl').textContent = stats.completed_reports || 0;
        statCards[3].querySelector('.text-3xl').textContent = stats.critical_reports || 0;
      }
    }
  } catch (error) {
    console.error('Error loading dashboard stats:', error);
  }
}

function getSeverityColor(severity) {
  const colors = {
    'Critical': 'bg-red-100 text-red-800 border-red-300',
    'High': 'bg-orange-100 text-orange-800 border-orange-300',
    'Medium': 'bg-yellow-100 text-yellow-800 border-yellow-300',
    'Low': 'bg-green-100 text-green-800 border-green-300'
  };
  return colors[severity] || 'bg-gray-100 text-gray-800 border-gray-300';
}

function getStatusColor(status) {
  const colors = {
    'pending': 'bg-gray-100 text-gray-800',
    'in_progress': 'bg-blue-100 text-blue-800',
    'completed': 'bg-green-100 text-green-800',
    'closed': 'bg-purple-100 text-purple-800'
  };
  return colors[status] || 'bg-gray-100 text-gray-800';
}

async function loadReports() {
  try {
    const response = await fetch('/api/reports?limit=10');
    const result = await response.json();

    const reportsList = document.getElementById('reports-list');
    
    if (result.success && result.data && result.data.length > 0) {
      reportsList.innerHTML = result.data.map(report => `
        <div class="p-4 border border-gray-200 rounded-lg hover:shadow-lg transition">
          <div class="flex justify-between items-start mb-2">
            <h4 class="font-semibold text-gray-800">${report.title}</h4>
            <span class="text-xs font-medium px-2 py-1 rounded border ${getSeverityColor(report.severity)}">${report.severity}</span>
          </div>
          <p class="text-sm text-gray-600 mb-3 line-clamp-2">${report.description}</p>
          <div class="flex justify-between items-center text-xs">
            <span class="text-gray-500"><strong>Location:</strong> ${report.location?.city_name || 'Unknown'}</span>
            <span class="px-2 py-1 rounded text-xs font-medium ${getStatusColor(report.status)}">${report.status}</span>
          </div>
          <div class="mt-2 text-xs text-gray-400">
            <strong>Reporter:</strong> ${report.reporter_name || 'Anonymous'}
          </div>
        </div>
      `).join('');
    } else {
      reportsList.innerHTML = '<p class="text-gray-500 text-center text-sm col-span-full">No reports available</p>';
    }
  } catch (error) {
    console.error('Error loading reports:', error);
    const reportsList = document.getElementById('reports-list');
    if (reportsList) {
      reportsList.innerHTML = '<p class="text-red-500 text-center text-sm col-span-full">Error loading reports</p>';
    }
  }
}

async function loadAnimalSightings() {
  try {
    const response = await fetch('/api/sightings');
    const result = await response.json();

    const sightingsList = document.getElementById('sightings-list');
    
    if (result.success && result.data && result.data.length > 0) {
      // Display only the first 10 sightings
      const displaySightings = result.data.slice(0, 10);
      sightingsList.innerHTML = displaySightings.map(sighting => `
        <div class="p-4 border border-gray-200 rounded-lg hover:shadow-lg transition">
          <div class="flex justify-between items-start mb-2">
            <h4 class="font-semibold text-gray-800">${sighting.species?.common_name || 'Unknown Species'}</h4>
            <span class="text-xs font-medium px-2 py-1 rounded bg-blue-100 text-blue-800">${sighting.species?.category || 'Unknown'}</span>
          </div>
          <p class="text-sm text-gray-600 mb-3">${sighting.notes || 'No details provided'}</p>
          <div class="grid grid-cols-2 gap-2 text-xs">
            <span class="text-gray-500"><strong>Location:</strong> ${sighting.location?.city_name || 'Unknown'}</span>
            <span class="text-gray-500"><strong>Date:</strong> ${new Date(sighting.sighting_date).toLocaleDateString()}</span>
          </div>
          <div class="mt-2 text-xs text-gray-400">
            <strong>Reported by:</strong> ${sighting.observer_name || 'Anonymous'}
          </div>
        </div>
      `).join('');
    } else {
      sightingsList.innerHTML = '<p class="text-gray-500 text-center text-sm col-span-full">No animal sightings available</p>';
    }
  } catch (error) {
    console.error('Error loading animal sightings:', error);
    const sightingsList = document.getElementById('sightings-list');
    if (sightingsList) {
      sightingsList.innerHTML = '<p class="text-red-500 text-center text-sm col-span-full">Error loading sightings</p>';
    }
  }
}
