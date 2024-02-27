

const main_view = document.querySelector("main");

document.addEventListener("DOMContentLoaded", () => {

    // nav bar click listeners
    document.querySelector("#nav-notifications").addEventListener('click', load_notifications_page);
    document.querySelector("#nav-profile").addEventListener('click', load_profile_page);
    
});


function load_notifications_page(event) {
    main_view.innerHTML = "TODO: New notifications Page<br>";
}

function load_profile_page(event) {
    main_view.innerHTML = "TODO: Profile Page<br>";
}

