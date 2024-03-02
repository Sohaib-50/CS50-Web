import { make_component, strip_tags } from "./helpers.js";

document.addEventListener("DOMContentLoaded", () => {
    handle_form_button_state();

    document.querySelector("#article-form")
        .addEventListener('submit', handle_form_submission);
    
});

function handle_form_button_state() {
    document.querySelector("#article-form")
}

function handle_form_submission(event) {
    console.log("Handling form submission");

    clear_error_messages();

    const title_value = document.querySelector('#id_title').value.trim();
    if (title_value === '') {
        display_notification("Your article must have a title.");
        event.preventDefault();
        return;
    }

    const content_quill_value = document.querySelector("#quill-input-id_content").value.trim();
    const content_value = content_quill_value ?
        strip_tags(JSON.parse(content_quill_value).html)
        :
        content_quill_value;
    if (content_value === '') {
        display_notification("Please write some content.");
        event.preventDefault();
        return;
    }

}

function clear_error_messages() {
    document.querySelector('#notifications').innerHTML = '';
}

function display_notification(error_message) {
    
    document.querySelector('#notifications').appendChild(
        make_component(`
            <div class="notification">
                ${ error_message }
            </div>
        `)
    );

}

