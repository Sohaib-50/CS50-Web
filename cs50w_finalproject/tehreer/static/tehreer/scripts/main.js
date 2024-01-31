import { handle_header_scroll_visibility } from "./helpers.js";

document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("button#nav-collapse").addEventListener("click", toggle_collapsed_nav);

    handle_header_scroll_visibility();
});


function toggle_collapsed_nav() {
    let nav = document.querySelector("nav ul");
    nav.classList.toggle("collapsed");
}