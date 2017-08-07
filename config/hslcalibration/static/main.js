$(document).ready(function() {
  // Init and attach listener to range selectors
  $('[data-hsl]').ionRangeSlider({
      type: 'double',
      min: 0.0,
      max: 1.0,
      from: 0,
      to: 1,
      step: 0.001,
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
