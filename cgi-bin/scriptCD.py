#!/usr/bin/python3

import json
import cgi
import random
import math


# logic/functions


def new_game(size=5):
    possible_colors = ["green", "blue", "orange", "purple", "red"]
    sequence = []
    for i in range(size ** 2):
        sequence.append(possible_colors[random.randint(0, len(possible_colors) - 1)])

    return Rooster(size, sequence)


def do_move(data):
    #recreate board passed on by the json object
    sequence = data['board']
    size = int(math.sqrt(len(sequence)))
    board_move = Rooster(size, sequence)
    board_move.druppel(data['move'])
    return board_move




class Rooster:

    def __init__(self, n, sequence):

        # vullen van het bord met nullen
        self.width = n
        self.height = int(len(sequence) / n)
        self.rooster = [[0 for x in range(self.width)] for y in range(self.height)]

        # letters invullen, ook positie van * opslaan
        index = 0
        self.druppeltegel = (0,0)
        for i in range(self.height):
            for j in range(self.width):
                self.rooster[i][j] = sequence[index]
                index += 1

        # nodig in druppel methode
        self.changedSpots = set()

    def __str__(self):
        # afprinten van het huidige bord
        return '\n'.join([' '.join(['{}'.format(item) for item in row]) for row in self.rooster])

    def druppel(self, char):
        self.kleuren(char, self.druppeltegel[0], self.druppeltegel[1])
        self.changedSpots.clear()
        return self.__str__()

    def kleuren(self, char, row, column):
        # set die verandere vlekken bijhoud

        # kleur veranderen indien nodig
        changed = False
        if self.rooster[row][column] == char.lower() or self.rooster[row][column].isupper():
            self.rooster[row][column] = char
            self.changedSpots.add((row, column))
            changed = True
        if self.rooster[row][column] == "*":
            changed = True
            self.changedSpots.add((row, column))
        # indien het kleur verander is kijken naar alle omliggende kleuren, indien die gelijk zijn aan de char.lower
        # of een hoofdletter zijn, ze ook veranderen
        if changed:
            # letter erboven, enkel als de row groter is dan nul
            if row > 0:
                if (self.rooster[row - 1][column] == char.lower() or self.rooster[row - 1][column].isupper()) and (
                row - 1, column) not in self.changedSpots:
                    self.kleuren(char, row - 1, column)
            # letter eronder, enkel als de row niet de grootste is
            if row < self.height - 1:
                if self.rooster[row + 1][column] == char.lower() or self.rooster[row + 1][column].isupper() and (
                row + 1, column) not in self.changedSpots:
                    self.kleuren(char, row + 1, column)
            # letter links, enkel als de kolom niet nul is
            if column > 0:
                if (self.rooster[row][column - 1] == char.lower() or self.rooster[row][column - 1].isupper()) and (
                row, column - 1) not in self.changedSpots:
                    self.kleuren(char, row, column - 1)
            # letter rechts, enkel als de kolom niet gelijk is aan de breedte
            if column < self.width - 1:
                if (self.rooster[row][column + 1] == char.lower() or self.rooster[row][column + 1].isupper()) and (
                row, column + 1) not in self.changedSpots:
                    self.kleuren(char, row, column + 1)

    def druppels(self, chars):
        # alle gegeven druppels afzonderlijk aan druppel doorgeven
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
elif data['action'] == 'do_move':
    board = do_move(data)
    new_data["board"] = board.getRooster()
    new_data['moves'] = board.getAllColors()

'''
STUUR CGI ANTWOORD TERUG
'''

print("Content-Type: application/json")
print()

print(json.dumps(new_data))
