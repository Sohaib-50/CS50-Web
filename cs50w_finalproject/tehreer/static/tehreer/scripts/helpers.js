
function handle_header_scroll_visibility() {
    let header = document.querySelector("header");
    let prev_scroll_pos = window.scrollY;
    window.addEventListener("scroll", function () {
        let current_scroll_pos = window.scrollY;
        if (prev_scroll_pos > current_scroll_pos) {
            header.style.top = "0";
        }
        else if (prev_scroll_pos + 10 < current_scroll_pos) {
            header.style.top = `-${header.offsetHeight}px`;
        }
        prev_scroll_pos = current_scroll_pos;
    });
}

function toggle_nav_collapse() {
    let nav = document.querySelector("nav ul");
    nav.classList.toggle("collapsed");
}


function make_component(html) {
    const container = document.createElement('div');
    container.innerHTML = html;
    const component = container.firstElementChild;
    return component;
}


export { handle_header_scroll_visibility, toggle_nav_collapse, make_component };
