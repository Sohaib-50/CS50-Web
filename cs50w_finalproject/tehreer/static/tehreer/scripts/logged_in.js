document.addEventListener("DOMContentLoaded", () => {

    // nav bar click listeners
    document.querySelector("#nav-write").addEventListener('click', load_write_page);
    document.querySelector("#nav-notifications").addEventListener('click', load_notifications_page);
    document.querySelector("#nav-profile").addEventListener('click', load_profile_page);
    
});


function load_write_page(event) {
    document.querySelector("main").innerHTML += "TODO: New Article Writing Page<br>";
}

function load_notifications_page(event) {
    document.querySelector("main").innerHTML += "TODO: New notifications Page<br>";
}

function load_profile_page(event) {
    document.querySelector("main").innerHTML += "TODO: Profile Page<br>";
}

