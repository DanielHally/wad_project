/*
    Setup category links on page load
*/
$(document).ready(function() {
    // Setup category links
    for (link of $(".category-link")) {
        var params = new URLSearchParams();
        params.set(SEARCH_CATEGORY_PARAM, $(link).attr('category'));
        $(link).attr('href', '/gsr/search/?' + params);
    }
});
