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

    $('.reply-button').click(function() {
      const buttonText = $(this).text();
      const reviewId = $(this).data('review-id');
      if (buttonText === "Reply") {
        $(this).text("Close");
      }else {
        $(this).text("Reply");
      }
      $(`#reply-form-${reviewId}`).toggle();


  });

$('.show-replies').click(function(){
    const reviewId = $(this).data('review-id');
    const buttonText = $(this).text();

    if(buttonText === "Show replies") {
        $(this).text("Hide replies");
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
                    const replyText = '<div class="row">' +
                                          '<div class="col-md-1"></div>' +
                                              '<div class="col-md-10">' +
                                                  '<strong>' + username + '</strong>' +
                                                  '<p>' + comment + '</p>' + '<hr>'
                                              '</div>' +
                                          '</div>' +
                                      '</div>';
                    $('#replies-section-' + reviewId).append(replyText);
                });
            }
        });
    } else {
        $(this).text("Show replies");
    }
    $(`#replies-section-${reviewId}`).toggle()
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
        const username = data.username;
        const comment = data.comment;
        const replyText = '<div class="row">' +
                                          '<div class="col-md-1"></div>' +
                                              '<div class="col-md-10">' +
                                                  '<strong>' + username + '</strong>' +
                                                  '<p>' + comment + '</p>' + '<hr>'
                                              '</div>' +
                                          '</div>' +
                                      '</div>';
        $('#replies-section-' + reviewId).append(replyText);
    },
  });
});

