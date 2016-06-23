function display_url(url) {
  $('#display').text(url);
}

// ajax post request to save user's url to db
$('#encoder').on('submit', function(e) {
  var $this = $(this).val();
  $.ajax({
    type: "POST",
    url: '/encoder',
    data: {
      'original_url': $this,
    },
    success: function(url) {
      display_url(url);
    }
  });
});