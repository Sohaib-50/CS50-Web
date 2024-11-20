const main_view = document.querySelector("main");
const articles_view = main_view.querySelector(".articles");

document.addEventListener("DOMContentLoaded", () => {

    // nav bar click listeners
    document.querySelector("#nav-notifications").addEventListener('click', load_notifications_page);
    document.querySelector("#nav-profile").addEventListener('click', load_profile_page);

    load_home_page();

    
});


function load_notifications_page() {
    main_view.innerHTML = "TODO: New notifications Page<br>";
}

function load_profile_page() {
    main_view.innerHTML = "TODO: Profile Page<br>";
}

function load_home_page() {
    // articles_view.style.display = 'none';
    // console.log(main_view.querySelector(".articles"));
}

