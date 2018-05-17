/*
* Author: Lucas Belpaire
* */

var data = {
    action: '',
    board: '',
    moves: '',
    message: ''
};


function handleItem(valueOfItem, a) {
    let currentList = $('#listItems').children('option').map(function () {
        return $(this).text()
    }).get();

    let data = {
        action: a,
        value: valueOfItem,
        list: currentList
    };

    console.log(JSON.stringify(data));
    fetch('cgi-bin/scriptCD.py?data=' + JSON.stringify(data))
        .then(response => response.json())
        .then(data => {
            $('#listItems').children('option').remove();
            console.log(data)
            newItems = data['list'];
            console.log(newItems)
            let i = 0;
            for (let item of newItems) {
                console.log(item);
                $('#listItems').append($('<option>', {
                    value: i,
                    text: item
                }));
                i += 1;
            }
        });
}

function interactWithScript(data) {
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
                console.log(index);
                index += 1;
                let rowOfBoard = $("<div class='row'></div>").css({"display": "flex"});
                $.each(row, function (j, circle) {
                    $(rowOfBoard).append($('<div id="individualCircle"></div>').css({"background-color": circle, "border-radius": "50%", "width": "50px", "height": "50px"}));
                });
                $('#board').append(rowOfBoard);
            });
        })
}

function getCurrentBoard() {
    let board = [];
    let currentBoard = $('#board').children('.row').map(function () {
        return $(this).text()
    }).get();
    for (let i = 0; i < currentBoard.length; i++) {
        board.push(currentBoard[i].trim().split("\n"));
        for (let j = 0; j < board[i].length; j++) {
            board[i][j] = board[i][j].trim();
        }
    }

    return board;

}


$(document).ready(function () {

    data['action'] = 'new_game';
    interactWithScript(data);

    $('#addColor').click(function () {

        let currentBoard = getCurrentBoard();
        let selectedOption = $('#selectColors').find(":selected").text();
        data['action'] = "do_move";
        data['board'] = currentBoard;
        data['move'] = selectedOption;
        interactWithScript(data)
    });

    $('#newGame').click(function () {
        data['action'] = 'new_game';
        interactWithScript(data);
    });

});
