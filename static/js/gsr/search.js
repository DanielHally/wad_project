/*
    gsr/search.html page javascript
*/

/*
    HTML element ids
*/
const QUERY_INPUT = "#query"
const CATEGORY_SELECT = '#category-filter';
const RATING_SELECT = '#rating-method';
const SEARCH_FORM = "#search-form"

/*
    Submit the search options form
*/
function submitForm() {
    $(SEARCH_FORM).submit();
}

/*
    Setup select elements and category links on page load
*/
$(document).ready(function() {
    // Fill in form based on GET parameters
    var params = getUrlParams();
    if (params.has(SEARCH_QUERY_PARAM)) {
        $(QUERY_INPUT).val(params.get(SEARCH_QUERY_PARAM));
    }
    if (params.has(SEARCH_CATEGORY_PARAM)) {
        $(CATEGORY_SELECT).val(params.get(SEARCH_CATEGORY_PARAM));
    }
    if (params.has(SEARCH_RATING_PARAM)) {
        $(RATING_SELECT).val(params.get(SEARCH_RATING_PARAM));
    }

    // Submit form on category or rating change
    $(CATEGORY_SELECT).change(submitForm);
    $(RATING_SELECT).change(submitForm);

    // Setup category links
    for (link of $(".category-link")) {
        var params = getUrlParams();
        params.set(SEARCH_CATEGORY_PARAM, $(link).attr('category'));
        $(link).attr('href', buildParamUrl(params));
    }
});
