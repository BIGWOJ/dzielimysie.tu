document.addEventListener("DOMContentLoaded", () => {
    const swiperWrapper = document.querySelector(".swiper-wrapper");
    const prevButton = document.querySelector(".pre-btn");
    const nextButton = document.querySelector(".nxt-btn");

    const step = 300; 
    const autoScrollInterval = 3000; // 3 seconds
    let scrollDirection = 1; // 1 for right, -1 for left

    nextButton.addEventListener("click", () => {
        swiperWrapper.scrollBy({ left: step, behavior: "smooth" });
    });

    prevButton.addEventListener("click", () => {
        swiperWrapper.scrollBy({ left: -step, behavior: "smooth" });
    });

    setInterval(() => {
        const maxScrollLeft = swiperWrapper.scrollWidth - swiperWrapper.clientWidth;
        const currentScrollLeft = swiperWrapper.scrollLeft;

        if (currentScrollLeft >= maxScrollLeft && scrollDirection === 1) {
            scrollDirection = -1;
        } else if (currentScrollLeft <= 0 && scrollDirection === -1) {
            scrollDirection = 1;
        }

        swiperWrapper.scrollBy({ left: step * scrollDirection, behavior: "smooth" });
    }, autoScrollInterval);

    const divider = document.querySelector(".divider");
    divider.addEventListener("click", () => {
        const halfHeight = window.innerHeight / 1.5;
        window.scrollTo({ top: halfHeight, behavior: "smooth" });
    });
});
