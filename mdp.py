
import random

COLORS = ['red', 'yellow', 'green', 'blue']
NUMBERS = range(1,10)
SPECIAL_CARD_TYPES = ['skip', 'reverse', '+2']
BLACK_CARD_TYPES = ['wildcard', '+4']
dict_moves = {}

def make_cards():
    for i in range (0, 10):
        for col in COLORS:
            for num in NUMBERS:
                dict_moves[(col, num, i)] = random.randint(0, 200)/1000
            for special in SPECIAL_CARD_TYPES:
                dict_moves[(col, special, i)] = random.randint(0, 200)/1000
        for black in BLACK_CARD_TYPES:
            dict_moves[('black', black, i)] = random.randint(0, 200)/1000
make_cards()