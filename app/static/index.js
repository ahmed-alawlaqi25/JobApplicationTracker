const btn = document.getElementById("menu-btn");
const icon = btn.querySelector("i");

btn.addEventListener("click", () => {
    icon.classList.toggle("fa-bars");
    icon.classList.toggle("fa-xmark");
});