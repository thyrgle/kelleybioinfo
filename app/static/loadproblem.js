/**
 * Custom loader for problems. Utilized by both levels.js and ran initially by
 * the problems.html template. A custom render must be used instead of render
 * template beecause of the the level changes.
 */
$(function(level = 1) {
  $.ajax({
    type: 'POST',
    data: { level: level },
    success: function(response) {
      $('#problem-col').html(response);
    },
  });
});
