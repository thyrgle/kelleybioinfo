/**
 * Custom loader for problems. Utilized by both levels.js and ran initially by
 * the problems.html template. A custom render must be used instead of render
 * template beecause of the the level changes.
 */
$(function () {
  function loadProblem(level = 1) {
    $.ajax({
      type: 'POST',
      data: { level: level },
      success: function(response) {
        $('#problem-col').html(response);
      },
    });
  };

  // Listen for level change toggle.
  $('.btn-group').on('change', 'input[type=radio]', function() {
    loadProblem($('input[type=radio]:checked', '.btn-group').attr('name'));
  });

  // Load on problem submission.
  $('#problem-submit').click(function(e) {
    e.preventDefault();
    $.ajax({
      type: 'POST',
      data: $('#problem-form').serialize(),
      success: function(message) {
        Swal.fire({
          title: message == "success" ? "Correct!" : "Incorrect.",
          type: message,
        }).then((result) => {
          loadProblem(
            $('input[type=radio]:checked', '.btn-group').attr('name')
          );
        });
      }
    });
  });
  // Call this once on start up to load the initial problem.
  loadProblem();
});
