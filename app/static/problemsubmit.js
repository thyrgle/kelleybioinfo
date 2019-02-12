/**
 * Handles when a problem has been submitted.
 */
$(function () {
  $("#problem-submit").click(function(e) {
    e.preventDefault();
    var level = $("input[type=radio]:checked", ".btn-group").attr("name");
    $.ajax({
      type: "POST",
      data: $("#problem-form").serialize(),
      success: function(message) {
        Swal.fire({
          title: message == "success" ? "Correct!" : "Incorrect.",
          type: message,
        }).then((result) => {
          $.ajax({
            type: "POST",
            data: { level: level },
            success: function (response) {
              $('#problem-col').html(response);
            }
          });
        });
      }
    });
  });
});
