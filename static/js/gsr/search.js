/*
    gsr/search.html page javascript
*/

/*
    GET parameter names
*/
const QUERY_PARAM = 'query';
const CATEGORY_PARAM = 'category';
const RATING_PARAM = 'rating';

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
    Setup select elements on page load
*/
$(document).ready(function() {
    // Fill in form based on GET parameters
    var params = getUrlParams();
    if (params.has(QUERY_PARAM)) {
        $(QUERY_INPUT).val(params.get(QUERY_PARAM));
    }
    if (params.has(CATEGORY_PARAM)) {
        $(CATEGORY_SELECT).val(params.get(CATEGORY_PARAM));
    }
    if (params.has(RATING_PARAM)) {
        $(RATING_SELECT).val(params.get(RATING_PARAM));
    }

    // Submit form on category or rating change
    $(CATEGORY_SELECT).change(submitForm);
    $(RATING_SELECT).change(submitForm);

    // Setup category links
    for (link of $(".category-link")) {
        var params = getUrlParams();
        params.set(CATEGORY_PARAM, $(link).attr('category'));
        $(link).attr('href', buildParamUrl(params));
    }
});
