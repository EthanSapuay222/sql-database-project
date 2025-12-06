// Submission Report Configuration and Initialization

// Fetch and populate locations from database
async function loadLocations() {
  try {
    const response = await fetch('/api/locations');
    const data = await response.json();
    
    if (data.success) {
      const locationSelect = document.getElementById('location');
      
      // Clear existing options except the first one
      locationSelect.innerHTML = '<option value="">Select Location</option>';
      
      // Sort locations alphabetically by city name
      const sortedLocations = data.data.sort((a, b) => 
        a.city_name.localeCompare(b.city_name)
      );
      
      // Add options for each location
      sortedLocations.forEach(location => {
        const option = document.createElement('option');
        option.value = location.location_id;
        option.textContent = `${location.city_name} (${location.location_type})`;
        locationSelect.appendChild(option);
      });
      
      console.log('Locations loaded successfully:', sortedLocations.length);
    } else {
      console.error('Failed to load locations:', data.message);
      showMessage('Failed to load locations. Please refresh the page.', 'error');
    }
  } catch (error) {
    console.error('Error fetching locations:', error);
    showMessage('Error loading locations. Please refresh the page.', 'error');
  }
}

// Helper function to show messages
function showMessage(message, type = 'success') {
  const messageBox = document.getElementById('message-box');
  if (messageBox) {
    messageBox.textContent = message;
    
    if (type === 'success') {
      messageBox.className = 'mt-4 p-3 text-center rounded-lg bg-green-100 text-green-800';
    } else if (type === 'error') {
      messageBox.className = 'mt-4 p-3 text-center rounded-lg bg-red-100 text-red-800';
    }
    
    messageBox.classList.remove('hidden');
  }
}

// Helper function to capitalize first letter
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

document.addEventListener('DOMContentLoaded', function() {
  const reportForm = document.getElementById('report-form');
  const messageBox = document.getElementById('message-box');
  const userIdDisplay = document.getElementById('user-id-display');
  
  // Load locations on page load
  loadLocations();
  
  // Update status display
  if (userIdDisplay) {
    userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Form Ready';
  }
  
  // Handle form submission
  if (reportForm) {
    reportForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      // Get form data
      const title = document.getElementById('report-title').value;
      const description = document.getElementById('description').value;
      const category = document.getElementById('category').value;
      const locationId = document.getElementById('location').value;
      const severity = document.getElementById('severity').value;
      
      // Validate location is selected
      if (!locationId) {
        showMessage('Please select a location', 'error');
        return;
      }
      
      // Prepare data for API
      const reportData = {
        title: title,
        description: description,
        report_type: category,
        location_id: parseInt(locationId),
        severity: capitalizeFirstLetter(severity),
        reporter_name: 'Anonymous', // You can add input fields for these if needed
        reporter_contact: 'N/A',
        report_date: new Date().toISOString().split('T')[0]
      };
      
      // Update status
      if (userIdDisplay) {
        userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Submitting...';
      }
      
      try {
        const response = await fetch('/api/reports', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(reportData)
        });
        
        const result = await response.json();
        
        if (result.success) {
          showMessage('Report submitted successfully! Thank you for your contribution.', 'success');
          
          // Reset form after 2 seconds
          setTimeout(function() {
            reportForm.reset();
            messageBox.classList.add('hidden');
            
            // Reload locations to refresh the dropdown
            loadLocations();
          }, 2000);
          
          // Update status
          if (userIdDisplay) {
            userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Form Ready';
          }
        } else {
          showMessage(`Error: ${result.message}`, 'error');
          
          if (userIdDisplay) {
            userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Submission Failed';
          }
        }
      } catch (error) {
        console.error('Submission error:', error);
        showMessage('Failed to submit report. Please check your connection and try again.', 'error');
        
        if (userIdDisplay) {
          userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Connection Error';
        }
      }
    });
  }
});