/**
 * Deals with selection of a cell in a matrix. In particular, toggles the cell
 * between yellow and clear.
 */
$(function() {
  $(document.body).on('click', '.cell', function() {
    console.log("HERE");
    // TODO Refactor the if statement?
    $( this ).toggleClass( "selected-cell" );
    var answerInput = $( this ).find("input[value|='selected']");
    if (answerInput.val() === 'selected') {
      answerInput.val('selected-not');
    } else {
      answerInput.val('selected');
    }
  });
});
