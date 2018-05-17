/*
* Author: Lucas Belpaire
* */

var data = {
    action: '',
    board: '',
    moves: '',
    message: ''
};

let score = 0;

function interactWithScript(data) {
    $('#score').text('Score: '+score);
    fetch('cgi-bin/scriptCD.py?data=' + JSON.stringify(data), {credentials: 'same-origin'})
        .then(response => response.json())
        .then(data => {
            let newBoard = data['board'];
            let moves = data['moves'];

            //fill in all the options the player can select
            $('#selectColors').children('option').remove();
            $.each(moves, function (i, color) {
                $('#selectColors').append($('<option>', {
                    text: color
                }));
            });

            //fill in the board
            $('#board').children('div').remove();
            $('#board').css({"display": "flex", "flex-direction": "column"})
            let index = 0;
            $.each(newBoard, function (i, row) {
                index += 1;
                let rowOfBoard = $("<div class='row'></div>").css({"display": "flex"});
                $.each(row, function (j, circle) {
                    $(rowOfBoard).append($('<div id="'+circle+'"></div>').css({"background-color": circle, "border-radius": "50%", "width": "50px", "height": "50px"}));
                });
                $('#board').append(rowOfBoard);
            });

            if(data['message']){
                alert("Congratulations, you have won!\nYour score is: "+score);
            }

        })
}

function getCurrentBoard() {
    let currentBoard = $('#board').children().children('div').map(function () {
        return $(this).attr('id');
    }).get();
    return currentBoard;
}


$(document).ready(function () {

    data['action'] = 'new_game';
    interactWithScript(data);

    $('#addColor').click(function () {
        score += 1;
        let currentBoard = getCurrentBoard();
        let selectedOption = $('#selectColors').find(":selected").text();
        data['action'] = "do_move";
        data['board'] = currentBoard;
        data['move'] = selectedOption.toUpperCase();
        interactWithScript(data)
    });

    $('#newGame').click(function () {
        data['action'] = 'new_game';
        score = 0;
        interactWithScript(data);
    });

});
