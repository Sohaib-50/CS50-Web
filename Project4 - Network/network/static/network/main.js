import { message_component, notification_component, post_component, profile_component } from './components.js';
import { handle_element } from './utils.js';


let new_post_form;
let posts_view;
let profile_view;
let page_title;

document.addEventListener('DOMContentLoaded', async () => {

    // fetch required elements
    new_post_form = document.querySelector('#new-post-form');
    posts_view = document.querySelector('#posts-view');
    profile_view = document.querySelector('#profile-view');
    page_title = document.querySelector('#page-title');

    // add event listeners
    try {  // only add event listener if user is logged in, otherwise these divs won't exist
        new_post_form.onsubmit = create_new_post;
    } catch (error) {
        console.log(error);
    }
    handle_element('#nav-user', element => { element.onclick = () => load_profile_view(document.querySelector('#nav-user').firstChild.innerHTML) });
    handle_element('#nav-following', element => { element.onclick = () => load_posts_view(true) });
    handle_element('#nav-all-posts', element => { element.onclick = () => load_posts_view(false) });


    // show posts view (with all posts not just following) initially
    load_posts_view(false);
});


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


function load_posts(posts, profile = false) {
    console.log(`Loading ${posts.length} posts, profile: ${profile}`);
    const posts_div = profile ? profile_view.querySelector('#posts') : posts_view.querySelector('#posts');
    posts_div.innerHTML = "";  // clear posts


    if (!posts || posts.length === 0) {
        posts_div.innerHTML = "<p> <i> No posts </i> </p>";
        return;
    }


    // add posts to DOM
    posts.forEach(post => {
        posts_div.appendChild(post_component(post));
    });

    // pagination buttons
    posts_div.innerHTML += `
        <div id="pagination">
            <button type="button" id="pagination-previous">&langle;</button>
            <div id="pagination-pagecount">
                <span id="pagination-pagecount-current">1</span>
                / 
                <span id="pagination-pagecount-total">3</span>
            </div>
            <button type="button" id="pagination-next">&rangle;</button>
        </div>`;

}

async function get_posts(following) {
    let posts = [];

    // get posts from server
    const url = `/posts?following=${following}`;

    await fetch(url)
        .then(response => response.json())
        .then(data => {
            // console.log(data);
            posts = data.posts || [];
        })
        .catch(error => {
            console.error(error);
        });

    return posts;
}


function load_profile(username) {

    // call server to get user details
    const url = `/profile/${username}`;

    fetch(url)
        .then(response => {
            if (response.status === 200) {
                return response.json();
            } else {
                return response.json().then(data => {
                    throw new Error(data.error);
                });
            }
        })
        .then(data => {
            const add_follow_btn = "current_user_follows" in data;
            const following = add_follow_btn && data.current_user_follows;
            profile_view.querySelector('#profile').replaceWith(profile_component(data, add_follow_btn, following));
            load_posts(data.posts, true);
        })
        .catch(error => {
            console.error(error);
        });

}


function load_posts_view(following = false) {

    /* make ui changes */
    // views
    posts_view.style.display = "block";
    profile_view.style.display = "none";

    // nav items
    handle_element('#new-post', element => { element.style.display = following ? "none" : "block" });  // hide new post form area if viewing following posts
    if (following) {
        handle_element('#nav-following', element => { element.classList.add("active") });
        handle_element('#nav-all-posts', element => { element.classList.remove("active") });
    }
    else {
        handle_element('#nav-following', element => { element.classList.remove("active") });
        handle_element('#nav-all-posts', element => { element.classList.add("active") });
    }
    handle_element('#nav-user', element => { element.classList.remove("active") });

    // page title
    page_title.innerHTML = following ? "Posts Of People You Follow" : "All Posts";

    // load posts
    get_posts(following)
        .then(posts => {
            load_posts(posts);
        })
        .catch(error => {
            console.error(error);
        });
}

function load_profile_view(username) {
    /* make ui changes */
    // views
    posts_view.style.display = "none";
    profile_view.style.display = "block";

    // nav items
    handle_element('#nav-all-posts', element => { element.classList.remove("active") });
    handle_element('#nav-following', element => { element.classList.remove("active") });
    if (username === document.querySelector('#nav-user').firstChild.innerHTML) {
        handle_element('#nav-user', element => { element.classList.add("active") });
    }
    else {
        handle_element('#nav-user', element => { element.classList.remove("active") });
    }

    // page title
    page_title.innerHTML = "Profile";

    // load user's posts
    load_profile(username);
}


export { load_profile_view }