import { load_profile_view, get_posts } from "./main.js";
import { get_cookie } from "./utils.js";

function make_component(html) {
    const container = document.createElement('div');
    container.innerHTML = html;
    const component = container.firstElementChild;
    return component;
}

function message_component(message_text) {
    const component = make_component(`
    <div class="message">
        <div class="message-content">${message_text}</div>
        <button class="message-close close">&times;</button>
    </div>`);

    component.querySelector('.message-close').onclick = () => {
        component.remove();
    }

    return component;
}


function notification_component(notification_text) {
    return make_component(`
        <div class="notification">
            ${notification_text}
        </div>
    `);
}


function post_component(post) {
    const component = make_component(`
    <div class="post">

        <div class="post-header">

            <div class="post-info">
                <div class="post-timestamp">
                    [${post.created}]
                </div>
                <div class="post-username">
                    ${post.user}
                </div>
                said:
            </div>

            <div class="post-likes">
                <!-- like heart -->
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart"
                    viewBox="0 0 16 16">
                    <path
                        d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15" />
                </svg>
                <!-- likes count -->
                ${post.likes}
            </div>
        </div>

        <div class="post-body">
            <div class="post-content">
                ${post.content}
            </div>
            <div class="post-btns">
                    <button class="post-edit">
                        Edit
                    </button>
                    <button class="post-delete">
                        Delete
                    </button>
            </div>
        </div>


    </div>
    `);
    component.querySelector('.post-username').onclick = () => {
        load_profile_view(post.user);
    }

    return component;
}

function pagination_component(page_number, total_pages) {
    const component = make_component(`
        <div id="pagination">
            ${(page_number > 1) ?
            '<button type="button" id="pagination-previous">&langle;</button>'
            :
            ''
        }
            <div id="pagination-pagecount">
                <span id="pagination-pagecount-current">${page_number}</span>
                / 
                <span id="pagination-pagecount-total">${total_pages}</span>
            </div>
            ${(page_number < total_pages) ?
            '<button type="button" id="pagination-next">&rangle;</button>'
            :
            ''
        }
        </div>
    `);
    return component;
}

function posts_component(posts_page, following = null, username = null) {

    const component = make_component(`
        <div id="posts">
            
        </div>
    `);

    const posts = posts_page.posts
    if (!posts || posts.length === 0) {
        component.innerHTML = "<p> <i> No posts </i> </p>";
        return component;
    }

    // add posts
    posts.forEach(post => {
        component.appendChild(post_component(post));
    });

    // add pagination navigation
    const page_number = posts_page.page_number;
    const total_pages = posts_page.total_pages;
    const pagination_component = make_component(`
        <div id="pagination">
            ${(page_number > 1) ?
            '<button type="button" id="pagination-previous">&langle;</button>'
            :
            '<div>&nbsp;</div>'  // for stylistic purposes, to keep pagination centered, &nbsp; is a non-breaking space
        }
            <div id="pagination-pagecount">
                <span id="pagination-pagecount-current">${page_number}</span>
                / 
                <span id="pagination-pagecount-total">${total_pages}</span>
            </div>
            ${(page_number < total_pages) ?
            '<button type="button" id="pagination-next">&rangle;</button>'
            :
            '<div>&nbsp;</div>'  // for stylistic purposes, to keep pagination centered, &nbsp; is a non-breaking space
        }
        </div>
    `);
    component.appendChild(pagination_component);

    // add event listeners to pagination next and previous buttons
    const previous_btn = component.querySelector("#pagination-previous");
    if (previous_btn) {
        previous_btn.addEventListener('click', () => {
            get_posts(following, username, page_number - 1)
                .then(new_posts_page => {
                    console.log(`Getting page ${page_number - 1} of posts`);
                    component.replaceWith(posts_component(new_posts_page, following, username));
                });
        });
    }

    const next_btn = component.querySelector("#pagination-next");
    if (next_btn) {
        next_btn.addEventListener('click', () => {
            get_posts(following, username, page_number + 1)
                .then(new_posts_page => {
                    console.log(`Getting page ${page_number + 1} of posts`);
                    component.replaceWith(posts_component(new_posts_page, following, username));
                });
        });
    }

    return component;
}

function profile_component(user, add_follow_btn = false, current_user_following = false) {
    const component_html = `
        <div id="profile">
            <div id="profile-about">
                <h2 id="profile-username"> ${user.username} </h2>
                <div id="profile-stats">
                    <p> Followers: <span id="profile-followers-count"> ${user.followers_count} </span> </p>
                    <p> Following: <span id="profile-following-count"> ${user.following_count} </span> </p>
                </div>
            </div>
        </div>`;

    let component = make_component(component_html);

    if (add_follow_btn) {
        component.appendChild(make_component(`
            <div id="profile-follow">
                <button id="profile-follow-btn" class="btn btn-primary"> ${following ? 'Unfollow' : 'Follow'} </button>
            </div>`));
        component.querySelector('#profile-follow-btn').onclick = () => {
            const request = new Request(
                `profile/${user.username}`,
                {
                    method: 'PUT',
                    headers: { 'X-CSRFToken': get_cookie('csrftoken') },
                    mode: 'same-origin', // Do not send CSRF token to another domain.
                    body: JSON.stringify({
                        follow: !following
                    })
                }
            );
            fetch(request)
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
                    const current_followers_count = parseInt(component.querySelector('#profile-followers-count').innerHTML);
                    const updated_user = {
                        ...user,
                        followers_count: current_followers_count + (following ? -1 : 1)
                    }
                    component.replaceWith(profile_component(updated_user, add_follow_btn, !following));
                })
                .catch(error => {
                    console.error(error);
                });
        }
    }

    // display html formatted 
    console.log(component.innerHTML);

    return component;
}




export { message_component, notification_component, post_component, posts_component, profile_component };

