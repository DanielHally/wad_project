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
    $('.reply-button').click(function(){
    const reviewId = $(this).data('review-id');
    $(`#reply-form-${reviewId}`).toggle();
  });

  $('.show-replies').click(function(){
    const reviewId = $(this).data('review-id');
    const buttonText = $(this).text();

    if(buttonText === "Show replies") {
        $(this).text("Hide replies");
    } else {
        $(this).text("Show replies");
    }
    });

});



$(document).on('submit', '.reply_form', function(e){
  e.preventDefault();
  var reviewId = $(this).find('[name=review_id]').val();
  console.log($('#comment-' + reviewId).val())
  $.ajax({
    type: 'POST',
    url: 'create_reply/',
    data: {
      comment: $('#comment-' + reviewId).val(),
      review_id: reviewId,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(data){
        $(`#reply-form-${reviewId}`).toggle();
    },
  });
});

