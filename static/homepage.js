$(document).ready(function() {
    $('.display-contents').hide();
    $('.display').hide();
    $('.display-intro').hide();
    $('.copy-btn').hide();
})

function display_url(url) {
  $('.display-contents').show();
  $('.display').show();
  if (url == "Please submit a valid url.") {
    $('.new-url').val(url);
  } else {
    // $('.new-url').val("http://catt.ify/" + url);
    $('.new-url').val("http://localhost:5000/" + url);
    $('.display-intro').show();
    $('.copy-btn').show();
  }
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
$('.copy-btn').attr('title', 'Copy to clipboard').tooltip('fixTitle').tooltip('show');

clipboard.on('success', function(e) {
    console.info('Action:', e.action);
    console.info('Text:', e.text);
    console.info('Trigger:', e.trigger);
    $(e.trigger).attr('title', 'Copied').tooltip('fixTitle').tooltip('show');
    e.clearSelection();
});

clipboard.on('error', function(e) {
    console.error('Action:', e.action);
    console.error('Trigger:', e.trigger);
});

