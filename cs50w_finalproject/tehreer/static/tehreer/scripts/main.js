import { handle_header_scroll_visibility, toggle_nav_collapse } from "./helpers.js";
import { Articles } from "./components/articles.js"

document.addEventListener("DOMContentLoaded", initial_setup);

function initial_setup() {

    document.querySelector("button#nav-collapse").addEventListener("click", toggle_nav_collapse);
    handle_header_scroll_visibility();

    // const all_articles = 
    document.querySelector('main').appendChild(articles);
}




