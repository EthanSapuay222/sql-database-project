// Life on Land and Water - Tab Switching

document.addEventListener('DOMContentLoaded', function() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const landSpecies = document.getElementById('land-species');
  const waterSpecies = document.getElementById('water-species');
  
  tabButtons.forEach(button => {
    button.addEventListener('click', function() {
      const category = this.getAttribute('data-category');
      
      // Update active tab button styles
      tabButtons.forEach(btn => {
        btn.style.color = '#6b7280';
        btn.style.borderBottom = '3px solid transparent';
        btn.classList.remove('active');
      });
      
      this.style.color = '#4b553c';
      this.style.borderBottom = '3px solid #6d8e48';
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
});
