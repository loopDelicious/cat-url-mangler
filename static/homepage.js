function display_url(url) {
  $('.display').text(url);
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