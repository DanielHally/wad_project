/*
    gsr/search.html page javascript
*/


/*
    GET parameter names (sync with views.search)
*/
const QUERY_PARAM = 'query';
const CATEGORY_PARAM = 'category';
const RATING_PARAM = 'rating';

/*
    Element ids (sync with gsr/search.html)
*/
const QUERY_INPUT = "#query"
const QUERY_BUTTON = "#query-button"
const CATEGORY_SELECT = '#category';
const RATING_SELECT = '#rating-method';

/*
    Special category name for no filtering (sync with views.search)
*/
const ANY_CATEGORY = 'Any';

/*
    Default rating method
    Must be a valid name from models.Shop.RatingMethod
*/
const DEFAULT_RATING = 'Overall Rating';

/*
    Setup select elements on page load
*/
$(document).ready(function() {
    // Fill in query text based on GET parameters
    var query = getUrlParamOrDefault(QUERY_PARAM, "");
    $(QUERY_INPUT).val(query);

    // Fill in category dropdown based on GET parameters
    var category = getUrlParamOrDefault(CATEGORY_PARAM, ANY_CATEGORY);
    $(CATEGORY_SELECT).val(category);
    
    // Fill in sort method dropdown based on GET parameters
    var method = getUrlParamOrDefault(RATING_PARAM, DEFAULT_RATING);
    $(RATING_SELECT).val(method);

    // Update GET parameters on query submission
    $(QUERY_BUTTON).click(function() {
        setUrlParam(QUERY_PARAM, $(QUERY_INPUT).val());
    })

    // Update GET parameters on category change
    $(CATEGORY_SELECT).change(function() {
        setUrlParam(CATEGORY_PARAM, $(this).val());
    });

    // Update GET parameters on rating method change
    $(RATING_SELECT).change(function() {
        setUrlParam(RATING_PARAM, $(this).val());
    });
});
