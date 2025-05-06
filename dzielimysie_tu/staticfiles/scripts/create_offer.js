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

// Character counter
const textarea = document.getElementById('opis');
const charCount = document.getElementById('char-count');

textarea.addEventListener('input', () => {
    const length = textarea.value.length;
    charCount.textContent = `${length} / 1000 znaków`;
});


const file_input = document.getElementById('file_upload');
const previewImage = document.getElementById('preview_image');

file_input.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});
