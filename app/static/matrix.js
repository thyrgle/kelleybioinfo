$( ".cell" ).click(function() {
    // TODO Refactor the if statement?
    $( this ).toggleClass( "selected-cell" );
    var answerInput = $( this ).find("input[value|='selected']");
    if (answerInput.val() === 'selected') {
        answerInput.val('selected-not');
    } else {
        answerInput.val('selected');
    }
});
