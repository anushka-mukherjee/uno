import pgzrun
from random import shuffle, choice, randint
from itertools import product, repeat, chain
from threading import Thread
from time import sleep
from sys import exit

COLORS = ['red', 'yellow', 'green', 'blue']
ALL_COLORS = COLORS + ['black']
NUMBERS = list(range(10)) + list(range(1, 10))
SPECIAL_CARD_TYPES = ['skip', 'reverse', '+2']
COLOR_CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES * 2
BLACK_CARD_TYPES = ['wildcard', '+4']
CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES + BLACK_CARD_TYPES
dict_moves = {('red', 1, 0): 0.031, ('red', 2, 0): 0.168, ('red', 3, 0): 0.182, ('red', 4, 0): 0.116, ('red', 5, 0): 0.165, ('red', 6, 0): 0.036, ('red', 7, 0): 0.151, ('red', 8, 0): 0.125, ('red', 9, 0): 0.093, ('red', 'skip', 0): 0.058, ('red', 'reverse', 0): 0.031, ('red', '+2', 0): 0.159, ('yellow', 1, 0): 0.039, ('yellow', 2, 0): 0.137, ('yellow', 3, 0): 0.105, ('yellow', 4, 0): 0.05, ('yellow', 5, 0): 0.119, ('yellow', 6, 0): 0.096, ('yellow', 7, 0): 0.005, ('yellow', 8, 0): 0.018, ('yellow', 9, 0): 0.1, ('yellow', 'skip', 0): 0.098, ('yellow', 'reverse', 0): 0.015, ('yellow', '+2', 0): 0.134, ('green', 1, 0): 0.064, ('green', 2, 0): 0.06, ('green', 3, 0): 0.2, ('green', 4, 0): 0.123, ('green', 5, 0): 0.061, ('green', 6, 0): 0.113, ('green', 7, 0): 0.133, ('green', 8, 0): 0.183, ('green', 9, 0): 0.009, ('green', 'skip', 0): 0.152, ('green', 'reverse', 0): 0.078, ('green', '+2', 0): 0.134, ('blue', 1, 0): 0.073, ('blue', 2, 0): 0.006, ('blue', 3, 0): 0.065, ('blue', 4, 0): 0.2, ('blue', 5, 0): 0.04, ('blue', 6, 0): 0.15, ('blue', 7, 0): 0.134, ('blue', 8, 0): 0.197, ('blue', 9, 0): 0.122, ('blue', 'skip', 0): 0.049, ('blue', 'reverse', 0): 0.136, ('blue', '+2', 0): 0.152, ('black', 'wildcard', 0): 0.122, ('black', '+4', 0): 0.021, ('red', 1, 1): 0.111, ('red', 2, 1): 0.023, ('red', 3, 1): 0.028, ('red', 4, 1): 0.196, ('red', 5, 1): 0.186, ('red', 6, 1): 0.007, ('red', 7, 1): 0.16, ('red', 8, 1): 0.163, ('red', 9, 1): 0.032, ('red', 'skip', 1): 0.182, ('red', 'reverse', 1): 0.056, ('red', '+2', 1): 0.07, ('yellow', 1, 1): 0.015, ('yellow', 2, 1): 0.142, ('yellow', 3, 1): 0.179, ('yellow', 4, 1): 0.158, ('yellow', 5, 1): 0.093, ('yellow', 6, 1): 0.173, ('yellow', 7, 1): 0.076, ('yellow', 8, 1): 0.062, ('yellow', 9, 1): 0.026, ('yellow', 'skip', 1): 0.161, ('yellow', 'reverse', 1): 0.112, ('yellow', '+2', 1): 0.141, ('green', 1, 1): 0.178, ('green', 2, 1): 0.014, ('green', 3, 1): 0.025, ('green', 4, 1): 0.178, ('green', 5, 1): 0.143, ('green', 6, 1): 0.117, ('green', 7, 1): 0.025, ('green', 8, 1): 0.085, ('green', 9, 1): 0.178, ('green', 'skip', 1): 0.134, ('green', 'reverse', 1): 0.051, ('green', '+2', 1): 0.174, ('blue', 1, 1): 0.058, ('blue', 2, 1): 0.138, ('blue', 3, 1): 0.049, ('blue', 4, 1): 0.167, ('blue', 5, 1): 0.063, ('blue', 6, 1): 0.077, ('blue', 7, 1): 0.039, ('blue', 8, 1): 0.15, ('blue', 9, 1): 0.107, ('blue', 'skip', 1): 0.129, ('blue', 'reverse', 1): 0.066, ('blue', '+2', 1): 0.045, ('black', 'wildcard', 1): 0.009, ('black', '+4', 1): 0.061, ('red', 1, 2): 0.016, ('red', 2, 2): 0.044, ('red', 3, 2): 0.143, ('red', 4, 2): 0.04, ('red', 5, 2): 0.155, ('red', 6, 2): 0.029, ('red', 7, 2): 0.156, ('red', 8, 2): 0.096, ('red', 9, 2): 0.168, ('red', 'skip', 2): 0.177, ('red', 'reverse', 2): 0.103, ('red', '+2', 2): 0.125, ('yellow', 1, 2): 0.123, ('yellow', 2, 2): 0.156, ('yellow', 3, 2): 0.12, ('yellow', 4, 2): 0.139, ('yellow', 5, 2): 0.14, ('yellow', 6, 2): 0.136, ('yellow', 7, 2): 0.136, ('yellow', 8, 2): 0.058, ('yellow', 9, 2): 0.149, ('yellow', 'skip', 2): 0.18, ('yellow', 'reverse', 2): 0.143, ('yellow', '+2', 2): 0.128, ('green', 1, 2): 0.185, ('green', 2, 2): 0.067, ('green', 3, 2): 0.006, ('green', 4, 2): 0.174, ('green', 5, 2): 0.016, ('green', 6, 2): 0.153, ('green', 7, 2): 0.182, ('green', 8, 2): 0.141, ('green', 9, 2): 0.003, ('green', 'skip', 2): 0.039, ('green', 'reverse', 2): 0.042, ('green', '+2', 2): 0.173, ('blue', 1, 2): 0.163, ('blue', 2, 2): 0.194, ('blue', 3, 2): 0.166, ('blue', 4, 2): 0.113, ('blue', 5, 2): 0.057, ('blue', 6, 2): 0.073, ('blue', 7, 2): 0.01, ('blue', 8, 2): 0.071, ('blue', 9, 2): 0.047, ('blue', 'skip', 2): 0.104, ('blue', 'reverse', 2): 0.09, ('blue', '+2', 2): 0.093, ('black', 'wildcard', 2): 0.148, ('black', '+4', 2): 0.186, ('red', 1, 3): 0.086, ('red', 2, 3): 0.049, ('red', 3, 3): 0.04, ('red', 4, 3): 0.184, ('red', 5, 3): 0.102, ('red', 6, 3): 0.174, ('red', 7, 3): 0.093, ('red', 8, 3): 0.164, ('red', 9, 3): 0.185, ('red', 'skip', 3): 0.049, ('red', 'reverse', 3): 0.081, ('red', '+2', 3): 0.145, ('yellow', 1, 3): 0.001, ('yellow', 2, 3): 0.111, ('yellow', 3, 3): 0.173, ('yellow', 4, 3): 0.157, ('yellow', 5, 3): 0.083, ('yellow', 6, 3): 0.113, ('yellow', 7, 3): 0.106, ('yellow', 8, 3): 0.194, ('yellow', 9, 3): 0.092, ('yellow', 'skip', 3): 0.097, ('yellow', 'reverse', 3): 0.052, ('yellow', '+2', 3): 0.193, ('green', 1, 3): 0.059, ('green', 2, 3): 0.001, ('green', 3, 3): 0.131, ('green', 4, 3): 0.003, ('green', 5, 3): 0.042, ('green', 6, 3): 0.17, ('green', 7, 3): 0.067, ('green', 8, 3): 0.083, ('green', 9, 3): 0.141, ('green', 'skip', 3): 0.172, ('green', 'reverse', 3): 0.123, ('green', '+2', 3): 0.12, ('blue', 1, 3): 0.147, ('blue', 2, 3): 0.011, ('blue', 3, 3): 0.065, ('blue', 4, 3): 0.165, ('blue', 5, 3): 0.11, ('blue', 6, 3): 0.106, ('blue', 7, 3): 0.09, ('blue', 8, 3): 0.133, ('blue', 9, 3): 0.108, ('blue', 'skip', 3): 0.072, ('blue', 'reverse', 3): 0.15, ('blue', '+2', 3): 0.011, ('black', 'wildcard', 3): 0.012, ('black', '+4', 3): 0.164, ('red', 1, 4): 0.051, ('red', 2, 4): 0.053, ('red', 3, 4): 0.021, ('red', 4, 4): 0.011, ('red', 5, 4): 0.122, ('red', 6, 4): 0.188, ('red', 7, 4): 0.063, ('red', 8, 4): 0.022, ('red', 9, 4): 0.138, ('red', 'skip', 4): 0.045, ('red', 'reverse', 4): 0.033, ('red', '+2', 4): 0.059, ('yellow', 1, 4): 0.02, ('yellow', 2, 4): 0.114, ('yellow', 3, 4): 0.056, ('yellow', 4, 4): 0.027, ('yellow', 5, 4): 0.041, ('yellow', 6, 4): 0.13, ('yellow', 7, 4): 0.191, ('yellow', 8, 4): 0.012, ('yellow', 9, 4): 0.134, ('yellow', 'skip', 4): 0.175, ('yellow', 'reverse', 4): 0.117, ('yellow', '+2', 4): 0.065, ('green', 1, 4): 0.034, ('green', 2, 4): 0.061, ('green', 3, 4): 0.165, ('green', 4, 4): 0.188, ('green', 5, 4): 0.022, ('green', 6, 4): 0.186, ('green', 7, 4): 0.028, ('green', 8, 4): 0.03, ('green', 9, 4): 0.009, ('green', 'skip', 4): 0.047, ('green', 'reverse', 4): 0.073, ('green', '+2', 4): 0.043, ('blue', 1, 4): 0.182, ('blue', 2, 4): 0.132, ('blue', 3, 4): 0.164, ('blue', 4, 4): 0.082, ('blue', 5, 4): 0.093, ('blue', 6, 4): 0.163, ('blue', 7, 4): 0.052, ('blue', 8, 4): 0.198, ('blue', 9, 4): 0.076, ('blue', 'skip', 4): 0.108, ('blue', 'reverse', 4): 0.11, ('blue', '+2', 4): 0.067, ('black', 'wildcard', 4): 0.132, ('black', '+4', 4): 0.13, ('red', 1, 5): 0.115, ('red', 2, 5): 0.187, ('red', 3, 5): 0.006, ('red', 4, 5): 0.054, ('red', 5, 5): 0.098, ('red', 6, 5): 0.093, ('red', 7, 5): 0.025, ('red', 8, 5): 0.181, ('red', 9, 5): 0.187, ('red', 'skip', 5): 0.197, ('red', 'reverse', 5): 0.077, ('red', '+2', 5): 0.012, ('yellow', 1, 5): 0.04, ('yellow', 2, 5): 0.037, ('yellow', 3, 5): 0.04, ('yellow', 4, 5): 0.153, ('yellow', 5, 5): 0.041, ('yellow', 6, 5): 0.037, ('yellow', 7, 5): 0.061, ('yellow', 8, 5): 0.11, ('yellow', 9, 5): 0.146, ('yellow', 'skip', 5): 0.068, ('yellow', 'reverse', 5): 0.117, ('yellow', '+2', 5): 0.108, ('green', 1, 5): 0.192, ('green', 2, 5): 0.08, ('green', 3, 5): 0.1, ('green', 4, 5): 0.117, ('green', 5, 5): 0.072, ('green', 6, 5): 0.029, ('green', 7, 5): 0.16, ('green', 8, 5): 0.038, ('green', 9, 5): 0.077, ('green', 'skip', 5): 0.056, ('green', 'reverse', 5): 0.003, ('green', '+2', 5): 0.059, ('blue', 1, 5): 0.122, ('blue', 2, 5): 0.187, ('blue', 3, 5): 0.081, ('blue', 4, 5): 0.063, ('blue', 5, 5): 0.101, ('blue', 6, 5): 0.031, ('blue', 7, 5): 0.163, ('blue', 8, 5): 0.065, ('blue', 9, 5): 0.138, ('blue', 'skip', 5): 0.015, ('blue', 'reverse', 5): 0.188, ('blue', '+2', 5): 0.08, ('black', 'wildcard', 5): 0.07, ('black', '+4', 5): 0.166, ('red', 1, 6): 0.03, ('red', 2, 6): 0.185, ('red', 3, 6): 0.193, ('red', 4, 6): 0.168, ('red', 5, 6): 0.16, ('red', 6, 6): 0.035, ('red', 7, 6): 0.109, ('red', 8, 6): 0.076, ('red', 9, 6): 0.127, ('red', 'skip', 6): 0.006, ('red', 'reverse', 6): 0.013, ('red', '+2', 6): 0.017, ('yellow', 1, 6): 0.12, ('yellow', 2, 6): 0.054, ('yellow', 3, 6): 0.134, ('yellow', 4, 6): 0.118, ('yellow', 5, 6): 0.044, ('yellow', 6, 6): 0.054, ('yellow', 7, 6): 0.086, ('yellow', 8, 6): 0.183, ('yellow', 9, 6): 0.069, ('yellow', 'skip', 6): 0.08, ('yellow', 'reverse', 6): 0.134, ('yellow', '+2', 6): 0.157, ('green', 1, 6): 0.003, ('green', 2, 6): 0.186, ('green', 3, 6): 0.142, ('green', 4, 6): 0.055, ('green', 5, 6): 0.147, ('green', 6, 6): 0.132, ('green', 7, 6): 0.01, ('green', 8, 6): 0.017, ('green', 9, 6): 0.021, ('green', 'skip', 6): 0.048, ('green', 'reverse', 6): 0.177, ('green', '+2', 6): 0.098, ('blue', 1, 6): 0.131, ('blue', 2, 6): 0.038, ('blue', 3, 6): 0.175, ('blue', 4, 6): 0.047, ('blue', 5, 6): 0.093, ('blue', 6, 6): 0.137, ('blue', 7, 6): 0.065, ('blue', 8, 6): 0.134, ('blue', 9, 6): 0.025, ('blue', 'skip', 6): 0.038, ('blue', 'reverse', 6): 0.15, ('blue', '+2', 6): 0.165, ('black', 'wildcard', 6): 0.02, ('black', '+4', 6): 0.091, ('red', 1, 7): 0.122, ('red', 2, 7): 0.062, ('red', 3, 7): 0.024, ('red', 4, 7): 0.044, ('red', 5, 7): 0.006, ('red', 6, 7): 0.145, ('red', 7, 7): 0.111, ('red', 8, 7): 0.026, ('red', 9, 7): 0.181, ('red', 'skip', 7): 0.17, ('red', 'reverse', 7): 0.113, ('red', '+2', 7): 0.196, ('yellow', 1, 7): 0.006, ('yellow', 2, 7): 0.001, ('yellow', 3, 7): 0.139, ('yellow', 4, 7): 0.076, ('yellow', 5, 7): 0.147, ('yellow', 6, 7): 0.109, ('yellow', 7, 7): 0.125, ('yellow', 8, 7): 0.179, ('yellow', 9, 7): 0.043, ('yellow', 'skip', 7): 0.198, ('yellow', 'reverse', 7): 0.062, ('yellow', '+2', 7): 0.163, ('green', 1, 7): 0.027, ('green', 2, 7): 0.099, ('green', 3, 7): 0.199, ('green', 4, 7): 0.118, ('green', 5, 7): 0.168, ('green', 6, 7): 0.016, ('green', 7, 7): 0.199, ('green', 8, 7): 0.059, ('green', 9, 7): 0.063, ('green', 'skip', 7): 0.05, ('green', 'reverse', 7): 0.08, ('green', '+2', 7): 0.074, ('blue', 1, 7): 0.099, ('blue', 2, 7): 0.184, ('blue', 3, 7): 0.041, ('blue', 4, 7): 0.011, ('blue', 5, 7): 0.178, ('blue', 6, 7): 0.107, ('blue', 7, 7): 0.136, ('blue', 8, 7): 0.082, ('blue', 9, 7): 0.017, ('blue', 'skip', 7): 0.048, ('blue', 'reverse', 7): 0.126, ('blue', '+2', 7): 0.032, ('black', 'wildcard', 7): 0.063, ('black', '+4', 7): 0.025, ('red', 1, 8): 0.135, ('red', 2, 8): 0.074, ('red', 3, 8): 0.18, ('red', 4, 8): 0.185, ('red', 5, 8): 0.117, ('red', 6, 8): 0.113, ('red', 7, 8): 0.016, ('red', 8, 8): 0.031, ('red', 9, 8): 0.102, ('red', 'skip', 8): 0.063, ('red', 'reverse', 8): 0.198, ('red', '+2', 8): 0.071, ('yellow', 1, 8): 0.05, ('yellow', 2, 8): 0.0, ('yellow', 3, 8): 0.005, ('yellow', 4, 8): 0.162, ('yellow', 5, 8): 0.146, ('yellow', 6, 8): 0.029, ('yellow', 7, 8): 0.045, ('yellow', 8, 8): 0.038, ('yellow', 9, 8): 0.128, ('yellow', 'skip', 8): 0.041, ('yellow', 'reverse', 8): 0.089, ('yellow', '+2', 8): 0.134, ('green', 1, 8): 0.057, ('green', 2, 8): 0.178, ('green', 3, 8): 0.062, ('green', 4, 8): 0.072, ('green', 5, 8): 0.07, ('green', 6, 8): 0.075, ('green', 7, 8): 0.162, ('green', 8, 8): 0.116, ('green', 9, 8): 0.1, ('green', 'skip', 8): 0.037, ('green', 'reverse', 8): 0.029, ('green', '+2', 8): 0.119, ('blue', 1, 8): 0.036, ('blue', 2, 8): 0.032, ('blue', 3, 8): 0.042, ('blue', 4, 8): 0.106, ('blue', 5, 8): 0.188, ('blue', 6, 8): 0.169, ('blue', 7, 8): 0.196, ('blue', 8, 8): 0.118, ('blue', 9, 8): 0.079, ('blue', 'skip', 8): 0.165, ('blue', 'reverse', 8): 0.176, ('blue', '+2', 8): 0.192, ('black', 'wildcard', 8): 0.174, ('black', '+4', 8): 0.177, ('red', 1, 9): 0.16, ('red', 2, 9): 0.124, ('red', 3, 9): 0.125, ('red', 4, 9): 0.187, ('red', 5, 9): 0.056, ('red', 6, 9): 0.165, ('red', 7, 9): 0.185, ('red', 8, 9): 0.102, ('red', 9, 9): 0.008, ('red', 'skip', 9): 0.011, ('red', 'reverse', 9): 0.189, ('red', '+2', 9): 0.084, ('yellow', 1, 9): 0.197, ('yellow', 2, 9): 0.02, ('yellow', 3, 9): 0.1, ('yellow', 4, 9): 0.146, ('yellow', 5, 9): 0.038, ('yellow', 6, 9): 0.055, ('yellow', 7, 9): 0.025, ('yellow', 8, 9): 0.004, ('yellow', 9, 9): 0.123, ('yellow', 'skip', 9): 0.144, ('yellow', 'reverse', 9): 0.179, ('yellow', '+2', 9): 0.124, ('green', 1, 9): 0.037, ('green', 2, 9): 0.108, ('green', 3, 9): 0.009, ('green', 4, 9): 0.142, ('green', 5, 9): 0.048, ('green', 6, 9): 0.113, ('green', 7, 9): 0.186, ('green', 8, 9): 0.033, ('green', 9, 9): 0.065, ('green', 'skip', 9): 0.06, ('green', 'reverse', 9): 0.053, ('green', '+2', 9): 0.069, ('blue', 1, 9): 0.117, ('blue', 2, 9): 0.2, ('blue', 3, 9): 0.038, ('blue', 4, 9): 0.041, ('blue', 5, 9): 0.019, ('blue', 6, 9): 0.02, ('blue', 7, 9): 0.106, ('blue', 8, 9): 0.149, ('blue', 9, 9): 0.092, ('blue', 'skip', 9): 0.024, ('blue', 'reverse', 9): 0.134, ('blue', '+2', 9): 0.134, ('black', 'wildcard', 9): 0.059, ('black', '+4', 9): 0.123}


##core idea for representation and implementation below

color_types = ["Red", "Yellow", "Green", "Blue"]

""" color_value_types is a list of all the possible values that a color card
    can have. These are 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, Skip, Reverse, and 
    Draw 2."""
color_value_types = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip",
    "Rev", "+2"]

""" magic_value_types is a list of all the possible values that a magic card
    can have. These are Draw 4 and Change."""
magic_value_types = ["+4", "Change"]

""" Outputs the list which contains all of the cards in the shuffled deck.
    E.g. : (“Red”, “0”), (“Blue”, “9”), (“Green”, “Skip”), (“Yellow”, “Rev”)
    (“Magic”, “+4”), (“Magic”, “Change”)"""

# Eshita
class UnoCard:
    """
    This class shows a representation of one uno card. It has a color and 
    card type, both of which are valid according to the rules. Both the color
    and the card_type are represented as a string.
    """
    def __init__(self, color, c_type):
        self.color = color
        self.card_type = c_type
        self.changed_color = None
        self.sprite = Actor('{}_{}'.format(color, c_type))

    def __repr__(self):
        return '<UnoCard object: {} {}>'.format(self.color, self.card_type)


    def __format__(self, f):
        if f == 'full':
            return '{} {}'.format(self.color, self.card_type)
        else:
            return str(self)

    @property
    def _color(self):
        return self.changed_color if self.changed_color else self.color

    @property
    def changed_color(self):
        return self._changed_color

    @changed_color.setter
    def changed_color(self, color):
        if color is not None:
            if color not in COLORS:
                raise ValueError('Invalid color')
        self._changed_color = color

    def playable(self, top_card):
        """ Outputs True or False depending on if the action specified can be 
        played based on the current player's hand.
        Inputs: 
        action: The action that the player wants to do
        top_card: The card that is currently the top card in the discard pile
        E.g. If player_hand = [(“Red”, “0”), (“Blue”, “9”)], 
        action = (“Blue”, “9”), and top_card = ("Blue", "2") 
        then check_play would output True.
        If action = (Green, “7”), then check_play would output False.
        If top_card = (Red, “7”), then check_play would output False."""
        same_color = self._color == top_card.color
        same_type = self.card_type == top_card.card_type
        magic_type = top_card.color == 'black'
        return (same_color or same_type or magic_type)

# Eshita
class UnoPlayer:
    """
    This class represents a single player in the game. The player initially
    has a hand of 7 uno cards (here represented as a list). The class also
    assigns an ID number to each player, in order to keep track of whose
    turn it is.
    """
    def __init__(self, cards, player_id=None):
        self.hand = cards
        self.player_id = player_id

    def __repr__(self):
         if self.player_id is not None:
             return '<UnoPlayer object: player {}>'.format(self.player_id)
         else:
             return '<UnoPlayer object>'

    def __str__(self):
         if self.player_id is not None:
             return str(self.player_id)
         else:
             return repr(self)

    def can_play(self, current_card):
        """
        The functions returns True if the current player contains any card
        in their hand that is currently playable. If there is no card that can 
        be played, the function returns false
        """
        for card in self.hand:
            if current_card.playable(card) == True:
                return True
        return False
       

#Anushka
class UnoGame:
    """
    This class represents a single iteration of the Uno game. 
    
    Input: 
    players: int [inidcates number of players in this game]
    random: bool (default: True) [for random shuffling of deck]
    """
    def __init__(self, players, random=True):
        if not isinstance(players, int):
            raise ValueError('Invalid game: players must be integer')
        if not 2 <= players <= 15:
            raise ValueError('Invalid game: must be between 2 and 15 players')
        self.deck = self._create_deck(random=random)
        self.players = [
            UnoPlayer(self._deal_hand(), n) for n in range(players)
        ]
        self._player_cycle = ReversibleCycle(self.players)
        self._current_player = next(self._player_cycle)
        self._winner = None
        self._check_first_card()

    def __next__(self):
        """
        This function sets the current player to the next player in the cycle
        of turn-taking.
        """
        self._current_player = next(self._player_cycle)

    def _create_deck(self, random):
        """
        Creates and outputs a list of the complete set of Uno Cards. 
        If random is True (this is the deafult value), the
        deck will be shuffled, otherwise will be unshuffled.
        """
        color_cards = product(COLORS, COLOR_CARD_TYPES)
        black_cards = product(repeat('black', 4), BLACK_CARD_TYPES)
        all_cards = chain(color_cards, black_cards)
        deck = [UnoCard(color, card_type) for color, card_type in all_cards]
        if random:
            shuffle(deck)
            return deck
        else:
            return list(reversed(deck))

    def _deal_hand(self):
        """
        Since each player is dealt 7 cards, this function will return a list of 
        7 cards from the top of the deck, and then remove this dealing
        from the deck.
        """
        return [self.deck.pop() for i in range(7)]

    @property
    def current_card(self):
        return self.deck[-1]

    @property
    def is_active(self):
        for player in self.players:
            if(len(player.hand)<=0):
                return False 
        return True

    @property
    def current_player(self):
        return self._current_player

    @property
    def winner(self):
        return self._winner

    def play(self, player, card=None, new_color=None):
        """
        Functionality for the player to "play" a card.
        Inputs: 
        player: int representing index number of the current player
        card: int representing index number of card in player's hand/dealing

        Preconditions and Assumptins:
        It must be player's turn, and if card is given, it must be playable.
        If card is not given (None), the player picks up a card from the deck,
        and skips playing their turn.

        If the game is over, then raises an exception for this.
        """
        _player = self.players[player]
        if card is None:
            self._pick_up(_player, 1)
            next(self)
            return
        _card = _player.hand[card]
        if not self.current_card.playable(_card):
            raise ValueError(
                'Invalid card: {} not playable on {}'.format(
                    _card, self.current_card
                )
            )
        if _card.color == 'black':
            if new_color not in COLORS:
                raise ValueError(
                    'Invalid new_color: must be red, yellow, green or blue'
                )
        if not self.is_active:
            raise ValueError('Game is over')

        played_card = _player.hand.pop(card)
        self.deck.append(played_card)

        card_color = played_card.color
        card_type = played_card.card_type
        if card_color == 'black':
            self.current_card.changed_color = new_color
            if card_type == '+4':
                next(self)
                self._pick_up(self.current_player, 4)
        elif card_type == 'reverse':
            self._player_cycle.reverse()
        elif card_type == 'skip':
            next(self)
        elif card_type == '+2':
            next(self)
            self._pick_up(self.current_player, 2)

        if self.is_active:
            next(self)
        else:
            self._winner = _player
            self._print_winner()

    def _print_winner(self):
        """
        Prints the winner name if available, otherwise look up the index number.
        """
        if self.winner.player_id:
            winner_name = self.winner.player_id
        else:
            winner_name = self.players.index(self.winner)
        print("Player {} wins!".format(winner_name))


    def _pick_up(self, player, n):
        """
        Takes n cards from the deck and adds it to the player's
        hand.
        
        Inputs:

        player: player of type UnoPlayer
        n: int representing the number of cards
        """
        penalty_cards = [self.deck.pop(0) for i in range(n)]
        player.hand.extend(penalty_cards)

    def _check_first_card(self):
        if self.current_card.color == 'black':
            color = choice(COLORS)
            self.current_card.changed_color = color
            print("Selected random color for black card: {}".format(color))

# Lila
class ReversibleCycle:
    """
    Represents an interface to an iterable which can be infinitely cycled
    and can be reversed.
    Starts at the first item (index 0), unless reversed before first iteration,
    in which case starts at the last item.
    iterable: any finite iterable
    """
    def __init__(self, iterable):
        self._items = list(iterable)
        self._pos = None
        self._rev = False

    def __next__(self):
        if self.pos is None:
            self.pos = -1 if self._rev else 0
        else:
            self.pos = self.pos + self._delta
        return self._items[self.pos]

    @property
    def _delta(self):
        return -1 if self._rev else 1

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value % len(self._items)

    def reverse(self):
        """
        Reverse the order of the iterable.
        """
        self._rev = not self._rev

#Lila
class GameData:
    def __init__(self):
        self.picked_card = None
        self.picked_color = None
        self.color_selection_required = False
        self.log = ''

    @property
    def picked_card(self):
        picked_card = self._picked_card
        self.picked_card = None
        return picked_card

    @picked_card.setter
    def picked_card(self, value):
        self._picked_card = value

    @property
    def picked_color(self):
        picked_color = self._picked_color
        self.picked_color = None
        return picked_color

    @picked_color.setter
    def picked_color(self, value):
        self._picked_color = value


game_data = GameData()

#Anushka
class AIUnoGame:
    def __init__(self, players):
        self.game = UnoGame(players)
        self.player = choice(self.game.players)
        self.player_index = self.game.players.index(self.player)
        print('The game begins. You are Player {}.'.format(self.player_index))

    def __next__(self):
        game = self.game
        player = game.current_player
        player_id = player.player_id
        current_card = game.current_card
        num = 7
        if player == self.player:
            played = False
            while not played:
                card_index = None
                while card_index is None:
                    card_index = game_data.picked_card
                new_color = None
                if card_index is not False:
                    card = player.hand[card_index]
                    if not game.current_card.playable(card):
                        game_data.log = 'You cannot play that card'
                        continue
                    else:
                        game_data.log = 'You played card {:full}'.format(card)
                        if card.color == 'black' and len(player.hand) > 1:
                            game_data.color_selection_required = True
                            while new_color is None:
                                new_color = game_data.picked_color
                            game_data.log = 'You selected {}'.format(new_color)
                else:
                    card_index = None
                    game_data.log = 'You picked up'
                game.play(player_id, card_index, new_color)
                played = True
        elif player.can_play(game.current_card):
            temp_list = []
            for i, card in enumerate(player.hand):
                if game.current_card.playable(card):
                    temp_list.append(card)
            max_val = 0
            max_card = 0
            for card in temp_list:
                try:
                    if max_val < dict_moves[card.color, card.card_type, num]:
                        max_val = dict_moves[card.color, card.card_type, num]
                except:
                    print()

            for i, card in enumerate(player.hand):
                if game.current_card.playable(card):
                    if card.color == 'black':
                        new_color = choice(COLORS)
                    else:
                        new_color = None
                    game_data.log = "Player {} played {:full}".format(player, card)
                    game.play(player=player_id, card=i, new_color=new_color)
                    break
            
        else:
            game_data.log = "Player {} picked up".format(player)
            game.play(player=player_id, card=None)


    def print_hand(self):
        print('Your hand: {}'.format(
            ' '.join(str(card) for card in self.player.hand)
        ))

num_players = 3 
#can change the number of players, as long as num_player <10 and num_players>1

game = AIUnoGame(num_players)

WIDTH = 1200
HEIGHT = 800

deck_img = Actor('back')
color_imgs = {color: Actor(color) for color in COLORS}


def game_loop():
    while game.game.is_active:
        sleep(2)
        next(game)

game_loop_thread = Thread(target=game_loop)
game_loop_thread.start()

def draw_deck():
    deck_img.pos = (130, 70)
    deck_img.draw()
    current_card = game.game.current_card
    current_card.sprite.pos = (210, 70)
    current_card.sprite.draw()
    if game_data.color_selection_required:
        for i, card in enumerate(color_imgs.values()):
            card.pos = (290+i*80, 70)
            card.draw()
    elif current_card.color == 'black' and current_card.changed_color is not None:
        color_img = color_imgs[current_card.changed_color]
        color_img.pos = (290, 70)
        color_img.draw()

def draw_players_hands():
    for p, player in enumerate(game.game.players):
        color = 'red' if player == game.game.current_player else 'black'
        text = 'P{} {}'.format(p, 'wins' if game.game.winner == player else '')
        screen.draw.text(text, (0, 300+p*130), fontsize=100, color=color)
        for c, card in enumerate(player.hand):
            if player == game.player:
                sprite = card.sprite
            else:
                sprite = Actor('back')
            sprite.pos = (130+c*80, 330+p*130)
            sprite.draw()

def show_log():
    screen.draw.text(game_data.log, midbottom=(WIDTH/2, HEIGHT-50), color='black')

def update():
    screen.clear()
    screen.fill((255, 255, 255))
    draw_deck()
    draw_players_hands()
    show_log()

def on_mouse_down(pos):
    if game.player == game.game.current_player:
        for card in game.player.hand:
            if card.sprite.collidepoint(pos):
                game_data.picked_card = game.player.hand.index(card)
                print('Selected card {} index {}'.format(card, game.player.hand.index(card)))
        if deck_img.collidepoint(pos):
            game_data.picked_card = False
            print('Selected pick up')
        for color, card in color_imgs.items():
            if card.collidepoint(pos):
                game_data.picked_color = color
                game_data.color_selection_required = False