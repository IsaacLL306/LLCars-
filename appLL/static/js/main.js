document.addEventListener("DOMContentLoaded", function () {
    // Inicializar todos los carruseles dinámicamente
    const carousels = document.querySelectorAll(".carousel");

    carousels.forEach((carousel) => {
        const slides = carousel.querySelectorAll(".carousel-slide");
        const prevButton = carousel.querySelector(".prev");
        const nextButton = carousel.querySelector(".next");
        let currentSlide = 0;

        // Función para mostrar la diapositiva actual
        function showSlide(index) {
            slides.forEach((slide, i) => {
                slide.style.display = i === index ? "block" : "none";
            });
        }

        // Navegar a la diapositiva anterior
        prevButton.addEventListener("click", function () {
            currentSlide = (currentSlide === 0) ? slides.length - 1 : currentSlide - 1;
            showSlide(currentSlide);
        });

        // Navegar a la diapositiva siguiente
        nextButton.addEventListener("click", function () {
            currentSlide = (currentSlide === slides.length - 1) ? 0 : currentSlide + 1;
            showSlide(currentSlide);
        });

        // Mostrar la primera diapositiva al cargar
        showSlide(currentSlide);
    });
});
