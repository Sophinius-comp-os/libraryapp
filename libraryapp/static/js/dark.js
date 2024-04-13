// Check the user's preference for dark mode
const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

// Initialize the mode based on user's preference
let isDarkMode = prefersDarkMode;

// Function to toggle between dark and light mode
function toggleMode() {
    const body = document.body;
    isDarkMode = !isDarkMode;

    // Toggle the 'dark-mode' class on the body
    body.classList.toggle('dark-mode', isDarkMode);

    // Toggle dark mode for Bootstrap components
    toggleBootstrapDarkMode(isDarkMode);

    // Save the user's preference in local storage
    localStorage.setItem('darkMode', isDarkMode);
}

// Set initial mode based on user's preference or default to light mode
document.body.classList.toggle('dark-mode', isDarkMode);

// Listen for changes in the user's preference for dark mode
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    isDarkMode = e.matches;
    document.body.classList.toggle('dark-mode', isDarkMode);

    // Toggle dark mode for Bootstrap components
    toggleBootstrapDarkMode(isDarkMode);
});

// Check if the user has a preferred mode stored in local storage
const storedMode = localStorage.getItem('darkMode');
if (storedMode !== null) {
    isDarkMode = storedMode === 'true';
    document.body.classList.toggle('dark-mode', isDarkMode);

    // Toggle dark mode for Bootstrap components
    toggleBootstrapDarkMode(isDarkMode);
}

// Function to toggle dark mode for Bootstrap components
function toggleBootstrapDarkMode(isDarkMode) {
    const elementsToToggle = document.querySelectorAll('.navbar, .form-control, .table');
    
    elementsToToggle.forEach(element => {
        element.classList.toggle('data-bs-theme="dark"', isDarkMode);
        element.classList.toggle('bg-dark', isDarkMode);
        element.classList.toggle('text-light', isDarkMode);
    });
}
