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
        switch (message) {
          case "success":
            Swal.fire({
              title: "Correct!",
              type: "success",
            }).then((result) => {
              $.ajax({
                type: "POST",
                data: { level: level },
                success: function (response) {
                  $('#problem-col').html(response);
                }
              });
            });
            break;
          case "failure":
            Swal.fire({
              title: "Incorrect.",
              type: "error",
            }).then((result) => {
              $.ajax({
                type: "POST",
                data: { level: level },
                success: function (response) {
                  $('#problem-col').html(response);
                }
              });
            });
            break;
          default:
            console.log("Rip.");
          }
        }
      });
  });
});
