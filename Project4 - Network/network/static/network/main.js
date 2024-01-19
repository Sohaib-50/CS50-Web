import { message_component, notification_component, post_component, posts_component, profile_component } from './components.js';
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

    // test out notifications
    // setInterval(() => {
    //     document.querySelector('#notifications')
    //         .appendChild(notification_component("This is a test notification!"));
    // }, 2000);

});


function create_new_post() {

    new_post_form.classList.add("disabled");  // disable form

    // get form input values
    const content = new_post_form.querySelector("#new-post-content").value.trim();
    console.log(content);
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

            // add post to DOM
            document.querySelector('#posts')
                .insertBefore(post_component(data.post), document.querySelector('#posts').firstChild);
            document.querySelector('#posts').firstChild.classList.add("new-post");

            // notification
            document.querySelector('#notifications')
                .appendChild(notification_component("Post created."));

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


function load_posts(posts_page, profile = false, following = null, username = null) {
    console.log(`Loading ${posts_page.posts.length} posts, profile: ${profile}`);
    const posts_div = profile ? profile_view.querySelector('#posts') : posts_view.querySelector('#posts');
    posts_div.innerHTML = "";  // clear posts

    posts_div.replaceWith(posts_component(posts_page, following, username))
}

async function get_posts(following = null, username = null, page_number = 1) {
    let posts_page;

    // get posts from server
    const url = (following != null) ?
        `/posts/${page_number}?following=${following}`
        :
        `/posts/${page_number}?username=${username}`;

    await fetch(url)
        .then(response => response.json())
        .then(data => {
            posts_page = data;
        })
        .catch(error => {
            console.error(error);
        });

    return posts_page;
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
            const current_user_following = add_follow_btn && data.current_user_follows;
            profile_view.querySelector('#profile').replaceWith(profile_component(data, add_follow_btn, current_user_following));

            const posts_page = data.posts_page;
            const profile = true;
            const following = false;
            load_posts(posts_page, profile, following, username);
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
    const username = null;
    get_posts(following, username, 1)
        .then(posts_page => {
            const username = null;
            const profile = false;
            load_posts(posts_page, profile, following, username);
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
    if (document.querySelector('#nav-user')) {  // if user is not logged in, this element won't exist
        if (username === document.querySelector('#nav-user').firstChild.innerHTML) {
            handle_element('#nav-user', element => { element.classList.add("active") });
        }
        else {
            handle_element('#nav-user', element => { element.classList.remove("active") });
        }
    }

    // page title
    page_title.innerHTML = "Profile";

    // load user's posts
    load_profile(username);
}


export { load_profile_view, get_posts }