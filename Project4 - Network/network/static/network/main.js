let new_post_form;
document.addEventListener('DOMContentLoaded', () => {

    // fetch required elements
    new_post_form = document.querySelector('#new-post-form');
    
    // add event listeners
    new_post_form.onsubmit = create_new_post;

});


function create_new_post() {
    // disable form
    new_post_form.classList.add("disabled");

    const content = new_post_form.querySelector("#new-post-content").value;
    const CSRF_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(`content: ${content}\nCSRF Token: ${CSRF_token}`);

    const request = new Request(
        '/new_post',
        {
            method: 'PUT',
            headers: {'X-CSRFToken': CSRF_token},
            mode: 'same-origin', // Do not send CSRF token to another domain.
            body: JSON.stringify({
                content: content
            })
        }
    );

    fetch(request)
        .then(response => response.json())
        .then(data => {
            console.log(`Response:\n${data}`);
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            // re-enable form
            new_post_form.classList.remove("disabled");
        });

    return false;  // prevent default action
}
