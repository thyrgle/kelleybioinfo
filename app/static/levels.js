$(function() {
  $('.btn-group').on('change', 'input[type=radio]', function() {
    $.ajax({
      type: "POST",
      data: { level: $(this).attr("name") },
      success: function(response) {
        $('#problem-col').html(response);
      },
    });
  });
});
