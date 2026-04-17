const btn = document.getElementById("menu-btn");
const icon = btn.querySelector("i");
const overlay = document.querySelector(".nav-overlay");

btn.addEventListener("click", () => {
    // toggle icon
    icon.classList.toggle("fa-bars");
    icon.classList.toggle("fa-xmark");

    // toggle menu
    overlay.classList.toggle("active");
});