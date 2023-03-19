/*
    gsr/add_shop.html page javascript
*/

/*
    GET parameter names
*/
const GET_NEXT_PARAM = 'next';

/*
    HTML element ids
*/
const NEXT_INPUT = "#next";
const LOCATION_AUTOCOMPLETE_INPUT = "#location-autocomplete";
const LOCATION_TRUE_INPUT = "#location";

/*
    Setup hidden next input on page load
*/
$(document).ready(() => {
    $('#image_field').change(function () {
        const file = this.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = function (event) {
                $('#imgPreview').css('backgroundImage', 'url(' + event.target.result + ')');
                $('#imgPreview').html('');
            }
            reader.readAsDataURL(file);
        }
    });
});

/*
    Google maps API callback
*/
let autocomplete;
function initMap() {
    // Set up autocomplete location widget
    autocomplete = new google.maps.places.Autocomplete(
        $(LOCATION_AUTOCOMPLETE_INPUT)[0],
        {
            types: ['establishment'],
            componentRestrictions: {'country': ['GB']},
            fields: ['place_id', 'geometry', 'name']
        }
    );

    // Fill in hidden input with place id if valid
    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (place.geometry) {
            $(LOCATION_TRUE_INPUT).val(place.place_id);
        }
        else {
            $(LOCATION_TRUE_INPUT).val('');
        }
    });
}
