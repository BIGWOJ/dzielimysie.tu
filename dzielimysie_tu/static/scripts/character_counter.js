// Character counter
const textarea = document.getElementById("opis");
const charCount = document.getElementById("char-count");

function updateCharCount() {
    const length = textarea.value.length;
    charCount.textContent = `${length} / 1000 znaków`;
}

textarea.addEventListener("input", updateCharCount);

// Initialize on page load
updateCharCount();

const file_input = document.getElementById("file_upload");
const previewImage = document.getElementById("preview_image");

file_input.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewImage.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});
