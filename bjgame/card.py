"""Module to create Cards and Decks for Blackjack game"""
import random
from collections import namedtuple
Card = namedtuple('Card', ['rank', 'suit'])
class FrenchDeck:
    """Class to create cards and create decks"""
    card_suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    card_rank = ['Ace'] + [str(num) for num in range (2, 11)] + ['Jack', 'Queen', 'King']
    @staticmethod
    def card_values(card):
        """Function to initalize values to each card so we can add for blackjack"""
        if card.rank in ['Jack', 'Queen', 'King']:
            return 10
        if card.rank == 'Ace':
            return 11
        return int(card.rank)
    @classmethod
    def create_deck(cls, num_of_decks=8):
        """Function to make a deck of cards"""
        return [Card(rank, suit)
                for rank in cls.card_rank
                for suit in cls.card_suits
               ] * num_of_decks
    @staticmethod
    def shuffle_and_cut_card(deck):
        """Function to shuffle deck and insert cut card in a random location between 60 and 80"""
        random.shuffle(deck)
        cut_location = len(deck) - random.randint(60, 80)
        return deck, cut_location
