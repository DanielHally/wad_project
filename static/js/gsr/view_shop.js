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
        $(`#replies-section-${reviewId}`).toggle()
        $.ajax({
            type: 'GET',
            url: 'show_replies/',
            data: {
              review_id: reviewId,
            },
            success: function(data){
                const replies = data.replies;
                $('#replies-section-' + reviewId).empty();
                $.each(replies, function(index, reply) {
                    const username = reply[0];
                    const comment = reply[1];
                    const replyText = username + '<br>' + comment + '<br><br>';
                    $('#replies-section-' + reviewId).append(replyText);
                });
            }
        });
    } else {
        $(`#replies-section-${reviewId}`).toggle()
        $(this).text("Show replies");
    }
});




});



$(document).on('submit', '.reply_form', function(e){
  e.preventDefault();
  var reviewId = $(this).find('[name=review_id]').val();
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
        const username = data.username;
        const comment = data.comment;
        const replyText = username + '<br>' + comment + '<br><br>';
        $('#replies-section-' + reviewId).append(replyText);
    },
  });
});

