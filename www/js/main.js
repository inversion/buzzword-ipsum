$(document).ready(function () {
  'use strict';


  $('form#getText').submit(function(event) {
    $('#textOut').html('<p>Leveraging strategic architecture...</p><img src="images/ajax-loader.gif" alt="AJAX Loading Image" />');
    $.ajax({
      url: '/buzzwords?format=html',
      data: $(this).serialize()
    }).done(function( data, textStatus, jqXHR ) {
      $('#textOut').html(data);
    }).fail(function( jqXHR, textStatus, errorThrown ) {
      var errText;
      try {
        errText = JSON.parse(jqXHR.responseText).message;
      } catch(e) {
        errText = 'Something went wrong, we got "' + errorThrown + '". Sorry about that, we\'ll fix it soon.';
      }
      $('#textOut').html('<p><span style="color: red;">Error:</span> ' + errText + '</p>');
    });
    event.preventDefault();
  });
});
