document.addEventListener("DOMContentLoaded", () => {
    let signin_div = document.querySelector("#signin");
    let signup_div = document.querySelector("#signup");

    document.querySelectorAll(".auth_toggler").forEach((toggler) => {
        toggler.addEventListener("click", () => {
            console.log("click");
            if (signup_div.style.display === "flex") {
                signin_div.style.display = "flex";
                signup_div.style.display = "none";
            } else {
                signup_div.style.display = "flex";
                signin_div.style.display = "none";
            }
        });
    });
});