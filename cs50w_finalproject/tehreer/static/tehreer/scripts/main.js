document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("button#nav-collapse").addEventListener("click", toggle_collapsed_nav);
});


function toggle_collapsed_nav() {
    let nav = document.querySelector("nav ul");
    nav.classList.toggle("collapsed");
}