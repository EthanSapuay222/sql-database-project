// Submission Report Configuration and Initialization

// Tailwind configuration is handled in head, but form logic below
document.addEventListener('DOMContentLoaded', function() {
  const reportForm = document.getElementById('report-form');
  const messageBox = document.getElementById('message-box');
  
  if (reportForm) {
    reportForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Get form data
      const title = document.getElementById('report-title').value;
      const description = document.getElementById('description').value;
      const category = document.getElementById('category').value;
      const location = document.getElementById('location').value;
      const severity = document.getElementById('severity').value;
      
      // Show success message
      if (messageBox) {
        messageBox.textContent = 'Report submitted successfully!';
        messageBox.className = 'mt-4 p-3 text-center rounded-lg bg-green-100 text-green-800';
        messageBox.classList.remove('hidden');
        
        // Reset form after 2 seconds
        setTimeout(function() {
          reportForm.reset();
          messageBox.classList.add('hidden');
        }, 2000);
      }
    });
  }
  
  // Update status display
  const userIdDisplay = document.getElementById('user-id-display');
  if (userIdDisplay) {
    userIdDisplay.innerHTML = '<span class="font-bold">Status:</span> Form Ready';
  }
});
