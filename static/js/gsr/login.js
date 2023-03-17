/*
    gsr/login.html page javascript
*/

/*
    GET parameter names
*/
const GET_NEXT_PARAM = 'next';

/*
    HTML element ids
*/
const NEXT_INPUT = "#next"

/*
    Setup hidden next input on page load
*/
$(document).ready(function() {
    var params = getUrlParams();
    if (params.has(GET_NEXT_PARAM)) {
        $(NEXT_INPUT).val(params.get(GET_NEXT_PARAM));
    }
});
