document.addEventListener('DOMContentLoaded', () => {
  const darkModeToggle = document.getElementById('darkModeToggle');

  // Load dark mode preference from localStorage if available
  if (localStorage.getItem('dark-mode') === 'enabled') {
    document.body.classList.add('dark-mode');
    darkModeToggle.textContent = 'Light Mode'; // Set button text for dark mode
  } else {
    darkModeToggle.textContent = 'Dark Mode'; // Set button text for light mode
  }

  darkModeToggle.addEventListener('click', () => {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    localStorage.setItem('dark-mode', isDarkMode ? 'enabled' : 'disabled');
    darkModeToggle.textContent = isDarkMode ? 'Light Mode' : 'Dark Mode';
  });
});
