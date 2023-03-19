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
const NEXT_INPUT = "#next"

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
