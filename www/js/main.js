$(document).ready(function () {
  'use strict';

  $('form#getText').submit(function(event) {
    $.ajax({
      url: '/buzzwords?format=html',
      data: $(this).serialize()
    }).done(function( data, textStatus, jqXHR ) {
      $('div#textOut').html(data);
    });
    event.preventDefault();
  });
});
