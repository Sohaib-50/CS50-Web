document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".article-preview").forEach(article => {
        // const article_id = article.dataset.id;
        article.addEventListener("click", () => load_article_view(article.dataset.id));
    });
});

function load_article_view(article_id) {
    console.log("Clicked article ID:", article_id);
    let article;

    fetch(`/tehreer/api/article/${article_id}`)
        .then(response => response.json())
        .then(json => {
            article = json;
            document.querySelector(".home_view").style.display = 'none';
            document.querySelector(".article_view").style.display = 'block';
            document.querySelector(".article_view").innerHTML = JSON.stringify(article);
        });
}