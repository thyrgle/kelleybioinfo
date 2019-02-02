$( ".cell" ).click(function() {
    // TODO Refactor the if statement?
    $( this ).toggleClass( "selected-cell" );
    var answerInput = $( this ).find("input[value|='selected']");
    console.log(answerInput.val());
    if (answerInput.val() === 'selected') {
        answerInput.val('selected-not');
        console.log("HERE");
    } else {
        answerInput.val('selected');
        console.log("HERE2");
    }
});
