let text_input = document.querySelector('textarea[name="opinion_text"]');
text_input.value = '';

document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.stars i:not([name="given_opinion_star"])');
    let selectedRating = 0;
    
    stars.forEach((star, index) => {
        // Hover effect
        star.addEventListener('mouseover', () => {
            stars.forEach((s, i) => {
                s.classList.toggle('fa-solid', i <= index);
                s.classList.toggle('fa-regular', i > index);
            });
        });
        
        // Reset starts after leaving
        star.addEventListener('mouseleave', () => {
            stars.forEach((s, i) => {
                s.classList.toggle('fa-solid', i < selectedRating);
                s.classList.toggle('fa-regular', i >= selectedRating);
            });
        });
        
        // Selecting stars
        star.addEventListener('click', () => {
            selectedRating = index + 1;
            console.log(selectedRating);
        });
    });
});

function set_rating(value) {
    document.getElementById('rating_input').value = value;
}