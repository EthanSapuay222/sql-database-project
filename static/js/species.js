// Tab Switching & Modal

document.addEventListener('DOMContentLoaded', function() {
  // TAB SWITCHING
  const tabButtons = document.querySelectorAll('.tab-btn');
  const landSpecies = document.getElementById('land-species');
  const waterSpecies = document.getElementById('water-species');
  
  tabButtons.forEach(button => {
    button.addEventListener('click', function() {
      const category = this.getAttribute('data-category');
      
      // Update active tab button styles
      tabButtons.forEach(btn => {
        btn.classList.remove('active');
      });
      
      this.classList.add('active');
      
      // Show/hide species grids
      if (category === 'land') {
        landSpecies.style.display = 'grid';
        waterSpecies.style.display = 'none';
      } else if (category === 'water') {
        waterSpecies.style.display = 'grid';
        landSpecies.style.display = 'none';
      }
    });
  });


  // MODAL FUNCTIONALITY

  const modal = document.getElementById('species-modal');
  const modalClose = document.getElementById('modal-close');
  const animalCards = document.querySelectorAll('.animal-card');
  
  // Modal elements
  const modalImage = document.getElementById('modal-image');
  const modalName = document.getElementById('modal-name');
  const modalScientific = document.getElementById('modal-scientific');
  const modalStatus = document.getElementById('modal-status');
  const modalType = document.getElementById('modal-type');
  const modalTrend = document.getElementById('modal-trend');
  const modalSightings = document.getElementById('modal-sightings');
  const modalDescription = document.getElementById('modal-description');
  const modalHabitat = document.getElementById('modal-habitat');
  const modalDiet = document.getElementById('modal-diet');

  // Open modal when clicking on animal card or view button
  animalCards.forEach(card => {
    card.addEventListener('click', function(e) {
      // Prevent double triggers
      e.stopPropagation();
      
      // Get data from card attributes
      const name = this.dataset.name;
      const scientific = this.dataset.scientific;
      const type = this.dataset.type;
      const status = this.dataset.status;
      const trend = this.dataset.trend;
      const sightings = this.dataset.sightings;
      const description = this.dataset.description;
      const habitat = this.dataset.habitat;
      const diet = this.dataset.diet;
      const image = this.dataset.image;
      
      // Populate modal
      modalImage.src = image;
      modalImage.alt = name;
      modalName.textContent = name;
      modalScientific.textContent = scientific;
      modalType.textContent = type;
      modalSightings.textContent = sightings;
      modalDescription.textContent = description;
      modalHabitat.textContent = habitat;
      modalDiet.textContent = diet;
      
      // Set conservation status with appropriate styling
      modalStatus.textContent = status;
      modalStatus.className = 'modal-status-badge status-' + status.toLowerCase().replace(/ /g, '-');
      
      // Set trend with styling
      modalTrend.textContent = trend.charAt(0).toUpperCase() + trend.slice(1);
      modalTrend.className = 'modal-info-value trend-' + trend;
      
      // Show modal
      modal.classList.add('active');
      document.body.style.overflow = 'hidden'; // Prevent background scrolling
    });
  });

  // Close modal on close button click
  modalClose.addEventListener('click', function() {
    closeModal();
  });

  // Close modal on overlay click (outside content)
  modal.addEventListener('click', function(e) {
    if (e.target === modal) {
      closeModal();
    }
  });

  // Close modal on Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });

  function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = ''; // Restore scrolling
  }
});
