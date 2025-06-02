"""Module to implement player and dealer's hands"""

import pickle
import os

class Player:
    """Class to create player and dealer initlization"""
    def __init__(self, name):
        """Function initlization for player"""
        self.name = name
        self.hand = []
        self.balance = 100.00
        self.wager = 0.00
    def reset_hand(self):
        """Function to reset the hand of the player"""
        self.hand = []
    def save_player_info(self):
        """Function to save the player information when we exit game"""
        os.makedirs('players', exist_ok = True)
        with open(f'players/{self.name}.pkl', 'wb') as file_handle:
            pickle.dump(self, file_handle)
    @staticmethod
    def load_player_info(name):
        """Loads player information from previous save"""
        try:
            with open(f'players/{name}.pkl', 'rb') as file_handle:
                return pickle.load(file_handle)
        except FileNotFoundError:
            return Player(name)
class Dealer(Player):
    """Dealer class to initialize Dealer"""
    def __init__(self):
        """Function initlization for dealer"""
        super().__init__('Dealer')
        self.hidden_card = None
