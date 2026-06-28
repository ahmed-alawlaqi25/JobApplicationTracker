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

window.addEventListener("resize", () => {
    if (window.innerWidth > 768) {
        overlay.classList.remove("active");

        icon.classList.remove("fa-xmark");
        icon.classList.add("fa-bars");
    }
});


const trackerForm = document.querySelector("#tracker-form-start");

document.querySelector(".button-form-x")
    .addEventListener("click", () => {
        trackerForm.style.display = "none";
    });

document.querySelector(".cancel-button")
    .addEventListener("click", () => {
        trackerForm.style.display = "none";
    });


const addJobBtn = document.querySelector(".add-job-button");

addJobBtn.addEventListener("click", () => {
    trackerForm.style.display = "flex";
})

