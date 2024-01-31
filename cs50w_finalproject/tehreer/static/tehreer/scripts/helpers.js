

function handle_header_scroll_visibility() {
    let header = document.querySelector("header");
    let prev_scroll_pos = window.scrollY;
    window.addEventListener("scroll", function () {
        console.log("scrolling");
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

export { handle_header_scroll_visibility };
