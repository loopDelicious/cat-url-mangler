
// hide encoded url display section and elements
$(document).ready(function() {
    $('.display-contents').hide();
    $('.display').hide();
    $('.display-intro').hide();
    $('.copy-btn').hide();
})
// helper function to display encoded url
function display_url(url) {
  $('.display-contents').show();
  $('.display').show();
  if (url == "Please submit a valid url.") {
    $('.new-url').val(url);
  } else {
    // $('.new-url').val("http://catt.ify/" + url);
    var protocol = window.location.protocol;
    var host = window.location.hostname;
    var port = window.location.port;
    $('.new-url').val(protocol + "//" + host + ":" + port + "/" + url);
    $('.display-intro').show();
    $('.copy-btn').show();
  }
}

// ajax post request to save user's url to db
$('#encoder').on('submit', function(e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: '/cat_path',
    data: {
      'original_url': $('#notes').val(),
    },
    success: function(url) { 
      display_url(url);
    }
  });
});

// Clipboard.JS to copy new URL to clipboard
var clipboard = new Clipboard('.copy-btn');
$('.copy-btn').attr('title', 'Copy to clipboard').tooltip('fixTitle').tooltip('show');

clipboard.on('success', function(e) {
    console.info('Action:', e.action);
    console.info('Text:', e.text);
    console.info('Trigger:', e.trigger);
    $(e.target).attr('title', 'Copied').tooltip('fixTitle').tooltip('show');
    e.clearSelection();
});

clipboard.on('error', function(e) {
    console.error('Action:', e.action);
    console.error('Trigger:', e.trigger);
});

