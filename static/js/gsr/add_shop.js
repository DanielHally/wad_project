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
$(document).ready(()=>{
		  $('{{ form.picture }}').change(function(){
			const file = this.files[0];
			console.log(file);
			if (file){
			  let reader = new FileReader();
			  reader.onload = function(event){
				console.log(event.target.result);
				$('#imgPreview').attr('src', event.target.result);
			  }
			  reader.readAsDataURL(file);
			}
		  });
		});
