// if address is something like xxx.yyy.zzz/, goto xxx.yyy.zzz/#start
if (document.location.hash == '' || document.location.hash == '#') {
  document.location.hash = '#start';
}

$(document).ready(function() {
  $('.history-button').click(function(event) {
    if ($(this).data('movement') == 'forward') {
      var newLocation = $('.card:target').next('.card').attr('id');
      if (newLocation != undefined) { document.location.hash = newLocation; }
    }
    else {
      var newLocation = $('.card:target').prev('.card').attr('id');
      if (newLocation != undefined) { document.location.hash = newLocation; }
    }
  });

  $('#capture-calibration').click(function(event) {
    var buttonText = $(this).text();
    $(this).text('...');
    $(this).addClass('loading');
    $.get('http://localhost:5000/capture', function(result) {
      if (result == 'True'){
        $(this).text(buttonText);
      }
    });
  });
});
