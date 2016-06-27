function display_url(url) {
  $('.display').text("http://" + url);
}

// ajax post request to save user's url to db
$('#encoder').on('submit', function(e) {
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: '/encode_url',
    data: {
      'original_url': $('#notes').val(),
    },
    success: function(url) {
      display_url(url);
    }
  });
});

var clipboard = new Clipboard('.copy-btn');

clipboard.on('success', function(e) {
    console.info('Action:', e.action);
    console.info('Text:', e.text);
    console.info('Trigger:', e.trigger);
    e.clearSelection();
});

clipboard.on('error', function(e) {
    console.error('Action:', e.action);
    console.error('Trigger:', e.trigger);
});