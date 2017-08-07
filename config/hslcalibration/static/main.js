$(document).ready(function() {
  // Init and attach listener to range selectors
  $('[data-hsl]').ionRangeSlider({
      type: 'double',
      min: 0,
      max: 255,
      from: 0,
      to: 255,
      step: 0.5,
      grid: true,
      onChange: function(data) {
        changeHSL($(data.input).data('hsl'), data.from, data.to);
      }
    });

    // Set range selectors to current value
    $.ajax({
      type: 'POST',
      url: '/post',
      data: {action: 'getHSL'},
      success: function(result) {
        var hsl = JSON.parse(result);

        Object.keys(hsl).forEach(function(key) {
          $('[data-hsl=' + key + ']').data('ionRangeSlider').update({
            from: hsl[key]['min'],
            to: hsl[key]['max']
          });
        });
      }
    });

    // Event listener for save button
    $('#save').click(function(e) {
      $(this).html('. . .');

      $.ajax({
        type: 'POST',
        url: '/post',
        data: {action: 'saveHSL'},
        success: function(result) {
          if (result == 'True') {
            $('#save').html('👍');
            setTimeout( function(){
              $('#save').html('Save');
            }, 1000);
          }
        }
      });
    });
  });

function changeHSL(component, min, max) {
  var data = {
    action: 'changeHSL',
    component: component,
    min: min,
    max: max
  };

  $.ajax({
    type: 'POST',
    url: '/post',
    data: data
  });
}
