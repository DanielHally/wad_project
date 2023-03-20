/*
    Common Glasgow Shop Ratings JavaScript utilities
*/

////////////////////
// GET parameters //
////////////////////

/*
    Gets a value from parameters, or a default if the key isn't found
*/
function paramsGetOrDefault(params, key, defaultValue) {
    var ret = params.get(key);
    if (ret == null) {
        ret = defaultValue;
    }
    return ret;
}

/*
    Get the URL GET parameters
*/
function getUrlParams() {
    return new URL(window.location.href).searchParams;
}

/*
    Get a URL GET parameter
*/
function getUrlParam(key) {
    var params = getUrlParams();
    return params.get(key);
}

/*
    Get a URL GET parameter, or a default if the key isn't found
*/
function getUrlParamOrDefault(key, defaultValue) {
    var params = getUrlParams();
    return paramsGetOrDefault(params, key, defaultValue);
}

/*
    Set the GET parameters of the url
*/
function setUrlParams(params) {
    window.location.href = window.location.href.split('?')[0] + '?' + params;
}

/*
    Set a GET parameter of the url
*/
function setUrlParam(key, value) {
    var params = getUrlParams();
    params.set(key, value);
    setUrlParams(params);
}

/*
    Setup star tooltips
*/
$(document).ready(function() {
    for (var element of $(".gsr-rating-stars")) {
        var tooltip = new bootstrap.Tooltip(element);
    }
});
