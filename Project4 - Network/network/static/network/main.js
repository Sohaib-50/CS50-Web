import { message_component, notification_component, post_component } from './components.js';

let new_post_form;


document.addEventListener('DOMContentLoaded', () => {

    // fetch required elements
    new_post_form = document.querySelector('#new-post-form');

    // add event listeners
    new_post_form.onsubmit = create_new_post;

    const following = false;
    load_posts(following);
});


function load_posts(following) {
    let posts;
    const posts_div = document.querySelector('#posts');

    // call server to get posts
    const url = `/posts?following=${following}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            posts = data;

            if (posts.length === 0) {
                posts_div.innerHTML = "<p> <i> No posts </i> </p>";
                return;
            }

            // add posts to DOM
            posts.forEach(post => {
                posts_div.appendChild(post_component(post));
            });
        })
        .catch(error => {
            console.error(error);
        });
}

function create_new_post() {

    new_post_form.classList.add("disabled");  // disable form

    // get form input values
    const content = new_post_form.querySelector("#new-post-content").value.trim();
    const CSRF_token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // call server to add post
    const request = new Request(
        '/new_post',
        {
            method: 'PUT',
            headers: { 'X-CSRFToken': CSRF_token },
            mode: 'same-origin', // Do not send CSRF token to another domain.
            body: JSON.stringify({
                content: content
            })
        }
    );
    fetch(request)
        .then(response => {
            if (response.status === 201) {
                return response.json();
            } else {
                return response.json().then(data => {
                    throw new Error(data.error);
                });
            }
        })

        .then(data => {
            console.log(`Response:\n${JSON.stringify(data)}`);

            // notification
            document.querySelector('#notifications')
                .appendChild(notification_component("Post created successfully!"));
            
            // add post to DOM
            document.querySelector('#posts')
                .insertBefore(post_component(data.post), document.querySelector('#posts').firstChild);

            // clear form
            console.log("Clearing form");
            new_post_form.querySelector("#new-post-content").value = "";
        })

        .catch(error => {
            console.error(error);

            // notification
            document.querySelector('#notifications')
                .appendChild(notification_component(error.message));
        })

        .finally(() => {
            new_post_form.classList.remove("disabled");  // re-enable form
        });

    return false;  // prevent default action
}
