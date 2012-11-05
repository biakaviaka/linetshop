$(document).ready(function() {
  $('.sidebar-nav a').click(function(event) {
    event.preventDefault();
    var href = $(this).attr('href');
    
    $.ajax({
      url: href,
      context: $(this).parent(),
      statusCode: {
        404: function() {
          $(this).append('not found');
        }
      }
    }).done(function(data) {
        $(this).append(data.sidemenu);
    });
  });
});
