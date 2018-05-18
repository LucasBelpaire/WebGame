/*
* Author: Lucas Belpaire
* */

let data = {
    action: '',
    board: '',
    moves: '',
    message: '',
    co: ''
};

let score = 0;

function interactWithScript(data) {
    fetch('cgi-bin/scriptCD.py?data=' + JSON.stringify(data), {credentials: 'same-origin'})
        .then(response => response.json())
        .then(data => {
            let newBoard = data['board'];
            let moves = data['moves'];
            score = data['score'];

            $('#score').text('Score: '+score);

            //fill in all the options the player can select
            $('#selectColors').children('option').remove();
            $.each(moves, function (i, color) {
                $('#selectColors').append($('<option>', {
                    text: color
                }));
            });

            //fill in the board
            $('#board').children('div').remove();
            $('#board').css({"display": "flex", "flex-direction": "column"});
            let rowNumber = 0;
            let columnNumber = 0;
            $.each(newBoard, function (i, row) {
                columnNumber = 0;
                let rowOfBoard = $("<div></div>").css({"display": "flex"});
                $.each(row, function (j, circle) {
                    $(rowOfBoard).append($('<div class="clickable" data-row="'+rowNumber+'" data-column="'+columnNumber+'" id="'+circle+'"></div>').css({"background-color": circle, "border-radius": "50%", "width": "70px", "height": "70px"}));
                    columnNumber += 1;
                });
                $('#board').append(rowOfBoard);
                rowNumber += 1;
            });

            //if the player has won the game, send an alert and start a new game
            if(data['message']){
                alert("Congratulations, you have won!\nYour score is: "+score);
                data['action'] = 'new_game';
                score = 0;
                interactWithScript(data);
            }

        })
}

function getCurrentBoard() {
    return $('#board').children().children('div').map(function () {
        return $(this).attr('id');
    }).get();
}


$(document).ready(function () {

    data['action'] = 'new_game';
    interactWithScript(data);

    $('#newGame').click(function () {
        data['action'] = 'new_game';
        data['score'] = 0;
        score = 0;
        interactWithScript(data);
    });

});

//all elements on the board are clickable, if you click on an element it wil also add its position (row, column) to the json object.
$(document).on('click', ".clickable", function() {

    let currentBoard = getCurrentBoard();
    let selectedOption = $('#selectColors').find(":selected").text();
    let rowNumber = $(this).data("row");
    let columnNumber = $(this).data("column");
    data['action'] = "do_move";
    data['board'] = currentBoard;
    data['move'] = selectedOption.toUpperCase();
    data['co'] = [rowNumber, columnNumber];
    data['score'] = score;
    interactWithScript(data)
});
