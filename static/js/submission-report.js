// Fetch and populate locations from database for environmental report
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

// Fetch and populate species from database
async function loadSpecies() {
  try {
    const response = await fetch('/api/species');
    const data = await response.json();
    
    if (data.success) {
      const speciesSelect = document.getElementById('species');
      
      // Clear existing options except the first one
      speciesSelect.innerHTML = '<option value="">Select a Species</option>';
      
      // Sort species alphabetically by common name
      const sortedSpecies = data.data.sort((a, b) => 
        a.common_name.localeCompare(b.common_name)
      );
      
      // Add options for each species
      sortedSpecies.forEach(species => {
        const option = document.createElement('option');
        option.value = species.species_id;
        option.textContent = `${species.common_name} (${species.scientific_name})`;
        speciesSelect.appendChild(option);
      });
      
      console.log('Species loaded successfully:', sortedSpecies.length);
    } else {
      console.error('Failed to load species:', data.message);
      showMessage('Failed to load species. Please refresh the page.', 'error');
    }
  } catch (error) {
    console.error('Error fetching species:', error);
    showMessage('Error loading species. Please refresh the page.', 'error');
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
  const sightingForm = document.getElementById('sighting-form');
  const messageBox = document.getElementById('message-box');
  const userIdDisplay = document.getElementById('user-id-display');
  
  // Tab switching
  const tabEnvironmental = document.getElementById('tab-environmental');
  const tabSighting = document.getElementById('tab-sighting');
  const formEnvironmental = document.getElementById('form-environmental');
  const formSighting = document.getElementById('form-sighting');
  
  // Tab click handlers
  tabEnvironmental.addEventListener('click', function() {
    tabEnvironmental.classList.add('active');
    tabSighting.classList.remove('active');
    formEnvironmental.classList.remove('hidden');
    formSighting.classList.add('hidden');
    messageBox.classList.add('hidden');
  });
  
  tabSighting.addEventListener('click', function() {
    tabSighting.classList.add('active');
    tabEnvironmental.classList.remove('active');
    formSighting.classList.remove('hidden');
    formEnvironmental.classList.add('hidden');
    messageBox.classList.add('hidden');
  });
  
  // Load data on page load
  loadLocations();
  loadSpecies();
  
  // Set today's date as default for sighting date
  const today = new Date().toISOString().split('T')[0];
  const sightingDateInput = document.getElementById('sighting-date');
  if (sightingDateInput) {
    sightingDateInput.value = today;
  }
  
  // Update status display
  if (userIdDisplay) {
    userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Form Ready';
  }
  
  // Handle environmental report form submission
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
        reporter_name: 'Anonymous',
        reporter_contact: 'N/A',
        report_date: new Date().toISOString().split('T')[0]
      };
      
      // Update status
      if (userIdDisplay) {
        userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Submitting...';
      }
      
      try {
        const csrfToken = document.querySelector('input[name="csrf_token"]')?.value || '';
        const response = await fetch('/api/reports', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify(reportData)
        });
        
        const result = await response.json();
        
        if (result.success) {
          showMessage('Report submitted successfully! Thank you for your contribution.', 'success');
          
          // Reset form
          setTimeout(function() {
            reportForm.reset();
            messageBox.classList.add('hidden');
            loadLocations();
          }, 2000);
          
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
  
  // Handle animal sighting form submission
  if (sightingForm) {
    sightingForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      const formData = new FormData(sightingForm);
      const speciesId = formData.get('species');
      const locationId = formData.get('sighting-location');
      const numberObserved = formData.get('number-observed');
      const observerName = formData.get('observer-name');
      const observerContact = formData.get('observer-contact');
      const notes = formData.get('sighting-notes');
      const sightingDate = formData.get('sighting-date');
      
      // Validate required fields
      if (!speciesId || !locationId || !observerName || !observerContact || !sightingDate) {
        showMessage('Please fill in all required fields.', 'error');
        return;
      }
      
      // Prepare submission data
      const sightingData = {
        species_id: parseInt(speciesId),
        location_id: parseInt(locationId),
        number_observed: parseInt(numberObserved) || 1,
        observer_name: observerName,
        observer_contact: observerContact,
        notes: notes || null,
        sighting_date: sightingDate
      };
      
      if (userIdDisplay) {
        userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Submitting...';
      }
      
      try {
        const csrfToken = document.querySelector('input[name="csrf_token"]')?.value || '';
        const response = await fetch('/api/sightings', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify(sightingData),
        });
        
        const result = await response.json();
        console.log('Sighting submission response:', result);
        
        if (result.success) {
          showMessage('Animal sighting submitted successfully! Thank you for contributing.', 'success');
          if (userIdDisplay) {
            userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Form Ready';
          }
          
          // Reset form
          setTimeout(function() {
            sightingForm.reset();
            document.getElementById('number-observed').value = '1';
            messageBox.classList.add('hidden');
          }, 2000);
          
        } else {
          showMessage(`Submission failed: ${result.message}`, 'error');
          if (userIdDisplay) {
            userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Submission Failed';
          }
        }
      } catch (error) {
        console.error('Error submitting sighting:', error);
        showMessage('An error occurred while submitting. Please try again.', 'error');
        if (userIdDisplay) {
          userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Error occurred';
        }
      }
    });
  }
});