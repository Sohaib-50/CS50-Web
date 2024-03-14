document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".article-preview").forEach(article => {
        // const article_id = article.dataset.id;
        article.addEventListener("click", () => load_article_view(article.dataset.id));
    });
});


function load_home_view() {
    document.querySelector("#home_view").style.display = 'flex';
    document.querySelector("#article_view").style.display = 'none';
}

function load_article_view(article_id) {
    console.log("Clicked article ID:", article_id);
    let article;

    fetch(`/tehreer/api/article/${article_id}`)
        .then(response => response.json())
        .then(json => {
            article = json;
            document.querySelector("#home_view").style.display = 'none';
            document.querySelector("#article_view").style.display = 'flex';
            // document.querySelector(".article_view").innerHTML = JSON.stringify(article);
            history.pushState({articleId: article_id}, null, `article/${article_id}/`);
        });
}


window.addEventListener('popstate', function(event) {
    if (event.state && event.state.articleId) {
        load_article_view(event.state.articleId);
    } else {
        load_home_view();
    }
});