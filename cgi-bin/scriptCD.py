#!/usr/bin/python3
#Author: Lucas Belpaire

import json
import cgi
import random
import math


def new_game(size=5):
    possible_colors = ["green", "blue", "orange", "purple", "red"]
    sequence = []
    for i in range(size ** 2):
        sequence.append(possible_colors[random.randint(0, len(possible_colors) - 1)])
    return Rooster(size, sequence)


def do_move(data):
    # recreate board passed on by the json object
    # check if the coordinates are (0,0), which is the only allowed value for this game
    sequence = data['board']
    size = int(math.sqrt(len(sequence)))
    board_move = Rooster(size, sequence)
    new_data['score'] = data['score']
    if data['co'] == [0, 0]:
        board_move.druppel(data['move'])
        new_data['score'] += 1
        if board_move.gewonnen(data['move']):
            new_data['message'] = "won"
    return board_move


class Rooster:

    def __init__(self, n, sequence):

        # fill in the board with all zero's.
        self.width = n
        self.height = int(len(sequence) / n)
        self.rooster = [[0 for x in range(self.width)] for y in range(self.height)]

        # fill in the color sequence
        # the position of the 'druppeltegel' also gets saved.
        index = 0
        self.druppeltegel = (0, 0)
        for i in range(self.height):
            for j in range(self.width):
                self.rooster[i][j] = sequence[index]
                index += 1

        # set will get used in the 'druppel' method.
        self.changedSpots = set()

    def __str__(self):
        # prints the current state of the board
        return '\n'.join([' '.join(['{}'.format(item) for item in row]) for row in self.rooster])

    def druppel(self, char):
        self.kleuren(char, self.druppeltegel[0], self.druppeltegel[1])
        self.changedSpots.clear()
        return self.__str__()

    def kleuren(self, char, row, column):

        changed = False
        if self.rooster[row][column] == char.lower() or self.rooster[row][column].isupper():
            self.rooster[row][column] = char
            self.changedSpots.add((row, column))
            changed = True
        if self.rooster[row][column] == "*":
            changed = True
            self.changedSpots.add((row, column))
        if changed:
            if row > 0:
                if (self.rooster[row - 1][column] == char.lower() or self.rooster[row - 1][column].isupper()) and \
                        (row - 1, column) not in self.changedSpots:
                    self.kleuren(char, row - 1, column)
            if row < self.height - 1:
                if self.rooster[row + 1][column] == char.lower() or self.rooster[row + 1][column].isupper() and \
                        (row + 1, column) not in self.changedSpots:
                    self.kleuren(char, row + 1, column)
            if column > 0:
                if (self.rooster[row][column - 1] == char.lower() or self.rooster[row][column - 1].isupper()) and \
                        (row, column - 1) not in self.changedSpots:
                    self.kleuren(char, row, column - 1)
            if column < self.width - 1:
                if (self.rooster[row][column + 1] == char.lower() or self.rooster[row][column + 1].isupper()) and \
                        (row, column + 1) not in self.changedSpots:
                    self.kleuren(char, row, column + 1)

    def druppels(self, chars):
        for char in chars:
            self.druppel(char)
        return self.__str__()

    def gewonnen(self, char):
        for i in range(self.height):
            for j in range(self.width):
                if self.rooster[i][j] != "*" and self.rooster[i][j] != char:
                    return False
        return True

    def getAllColors(self):
        colors = set()
        for i in range(self.height):
            for j in range(self.width):
                colors.add(self.rooster[i][j].lower())
        return sorted(list(colors))

    def getRooster(self):
        return self.rooster


# get the data
data = json.loads(cgi.FieldStorage().getvalue('data'))

new_data = dict()

if data['action'] == 'new_game':
    board = new_game()
    new_data['board'] = board.getRooster()
    new_data['moves'] = board.getAllColors()
    new_data['score'] = 0
elif data['action'] == 'do_move':
    board = do_move(data)
    new_data["board"] = board.getRooster()
    new_data['moves'] = board.getAllColors()

print("Content-Type: application/json")
print()

print(json.dumps(new_data))
