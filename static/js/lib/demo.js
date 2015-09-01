/**
 * Credit: 
 * Particleground demo
 * @author Jonathan Nicol - @mrjnicol
 */


$(document).ready(function() {
  $('#particles').particleground({
    dotColor: '#084250',
    lineColor: '#0A2937'
  });
  $('.intro').css({
    'margin-top': -($('.intro').height() / 2)
  });
});