$(document).ready(function () {
  'use strict';


  $('form#getText').submit(function(event) {
    $('#textOut').html('<p>Leveraging strategic architecture...</p><img src="images/ajax-loader.gif" alt="AJAX Loading Image" />');
    $.ajax({
      url: '/buzzwords?format=html',
      data: $(this).serialize()
    }).done(function( data, textStatus, jqXHR ) {
      $('#textOut').html(data);
    });
    event.preventDefault();
  });
});
