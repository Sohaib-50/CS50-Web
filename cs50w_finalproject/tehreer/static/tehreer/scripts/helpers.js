
function handle_header_scroll_visibility() {
    let header = document.querySelector("header");
    let explore = document.querySelector(".explore");
    let prev_scroll_pos = window.scrollY;
    window.addEventListener("scroll", function () {
        // console.log(header.getBoundingClientRect().bottom);
        let current_scroll_pos = window.scrollY;
        if (prev_scroll_pos > current_scroll_pos) {
            header.style.top = "0";
        } else if (prev_scroll_pos < current_scroll_pos) {
            header.style.top = `-${header.offsetHeight}px`;
        }
        explore.style.top = `${header.getBoundingClientRect().bottom }px`;
        prev_scroll_pos = current_scroll_pos;
    });
}

function toggle_nav_collapse() {
    let nav_ul = document.querySelector("nav ul");
    nav_ul.classList.toggle("collapsed");
}


function make_component(html) {
    const container = document.createElement('div');
    container.innerHTML = html;
    const component = container.firstElementChild;
    return component;
}

function strip_tags(html_string) {
    console.log(typeof(html_string));
    return html_string.replace(/<[^>]*>/g, '');
}


export { handle_header_scroll_visibility, toggle_nav_collapse, make_component, strip_tags };

