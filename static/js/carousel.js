const track = document.getElementById("projects-track");

if (track) {
    const cards = track.querySelectorAll(".project-card");
    const prevBtn = document.querySelector(".carousel-prev");
    const nextBtn = document.querySelector(".carousel-next");
    const total = cards.length;

    let current = 0;

    function render() {
        cards.forEach(function (card, i) {
            card.classList.remove("is-active", "is-prev", "is-next");

            if (i === current) {
                card.classList.add("is-active");
            } else if (i === (current - 1 + total) % total) {
                card.classList.add("is-prev");
            } else if (i === (current + 1) % total) {
                card.classList.add("is-next");
            }
        });
    }

    function move(step) {
        current = (current + step + total) % total;
        render();
    }

    if (total < 2) {
        prevBtn.style.display = "none";
        nextBtn.style.display = "none";
    }

    prevBtn.addEventListener("click", function () {
        move(-1);
    });

    nextBtn.addEventListener("click", function () {
        move(1);
    });

    render();
}