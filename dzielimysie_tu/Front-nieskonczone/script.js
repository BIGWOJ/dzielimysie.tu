document.addEventListener("DOMContentLoaded", () => {
    const swiperWrapper = document.querySelector(".swiper-wrapper");
    const prevButton = document.querySelector(".pre-btn");
    const nextButton = document.querySelector(".nxt-btn");

    const step = 300; 
    
    nextButton.addEventListener("click", () => {
        swiperWrapper.scrollBy({ left: step, behavior: "smooth" });
    });

    prevButton.addEventListener("click", () => {
        swiperWrapper.scrollBy({ left: -step, behavior: "smooth" });
    });
});
