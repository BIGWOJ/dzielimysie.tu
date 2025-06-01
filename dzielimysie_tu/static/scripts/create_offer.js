// Clear all inputs after refreshing the page
window.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('select');
    select.selectedIndex = 0;

    const inputs = document.querySelectorAll('input');
    const description_input = document.getElementById('opis');
    description_input.value = '';

    const textarea = document.getElementById('opis');
    if (textarea) {
        textarea.value = '';
    }

    const previewImage = document.getElementById('preview_image');
    if (previewImage) {
        previewImage.src = '';
        previewImage.style.display = 'none';
    }
});

