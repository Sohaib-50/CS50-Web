import { make_component, strip_tags } from "./helpers.js";

document.addEventListener("DOMContentLoaded", () => {

    // event listeners to enable/disable form based on whether title and content are present
    document.querySelector("#id_title").addEventListener("input", handle_form_button_state);
    document.querySelector(".ql-editor").addEventListener("keydown", handle_form_button_state);
    document.querySelector(".ql-editor").addEventListener("input", handle_form_button_state);

    // event listener for form allowing it to be submitted only if both title and content are present
    document.querySelector("#article-form").addEventListener("submit", handle_form_submission);

});


function handle_form_button_state() {
    const article_title = document.querySelector("#id_title").value.trim();

    const article_quill_content = document.querySelector("#quill-input-id_content").value.trim();
    const article_content = article_quill_content ? strip_tags(JSON.parse(article_quill_content).html).trim() : '';

    document.querySelector("#article-form-publish").disabled = article_title === '' || article_content === '';
}

function handle_form_submission(event) {

    clear_toasts();

    const title_value = document.querySelector('#id_title').value.trim();
    if (title_value === '') {
        display_toast("Your article must have a title.");
        event.preventDefault();
        return;
    }

    const content_quill_value = document.querySelector("#quill-input-id_content").value.trim();
    const content_value = content_quill_value ?
        strip_tags(JSON.parse(content_quill_value).html)
        :
        content_quill_value;
    if (content_value === '') {
        display_toast("Please write some content.");
        event.preventDefault();
        return;
    }

}

function clear_toasts() {
    document.querySelector('#toasts').innerHTML = '';
}


function display_toast(toast_content) {

    document.querySelector('#toasts').appendChild(
        make_component(`
            <div class="toast">
                ${toast_content}
            </div>
        `)
    );

}

