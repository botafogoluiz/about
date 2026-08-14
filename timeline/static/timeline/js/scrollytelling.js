(function () {
    var sections = document.querySelectorAll("[data-bg]");
    var layers = [document.getElementById("bg-layer-a"), document.getElementById("bg-layer-b")];
    var dots = document.querySelectorAll(".timeline-dot");
    var activeLayer = 0;

    if (!sections.length || !layers[0] || !layers[1] || !("IntersectionObserver" in window)) {
        return;
    }

    function setBackground(url) {
        var nextLayer = layers[1 - activeLayer];
        var currentLayer = layers[activeLayer];
        nextLayer.style.backgroundImage = "url(" + url + ")";
        nextLayer.classList.add("visible");
        currentLayer.classList.remove("visible");
        activeLayer = 1 - activeLayer;
    }

    function setActiveDot(index) {
        dots.forEach(function (dot, i) {
            dot.classList.toggle("active", i === index);
        });
    }

    setBackground(sections[0].dataset.bg);
    setActiveDot(0);

    var observer = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    setBackground(entry.target.dataset.bg);
                    setActiveDot(Number(entry.target.dataset.index));
                }
            });
        },
        { threshold: 0.5 }
    );

    sections.forEach(function (section) {
        observer.observe(section);
    });
})();
