"""This script creates the Black Jack game functionality"""
import time
import os
from .player import Player, Dealer
from .card import FrenchDeck
def slow_print(text):
    """This function makes the text slow using sleep"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()
def clear_console():
    """This function clears the console"""
    os.system('cls' if os.name == 'nt' else 'clear')
def hand_value(hand):
    """This Function calculates the hand value"""
    total_value, aces = 0, 0
    for card in hand:
        val = FrenchDeck.card_values(card)
        total_value += val
        if card.rank == 'Ace':
            aces += 1
    while total_value > 21 and aces:
        total_value -= 10
        aces -= 1
    return total_value
class BlackJackGame():
    """This class creates the blackjack game"""
    def __init__(self):
        """Initlization for blackjack class"""
        os.makedirs('players', exist_ok = True)
        self.deck = FrenchDeck.create_deck()
        self.deck, self.cut_card_position = FrenchDeck.shuffle_and_cut_card(self.deck)
        self.players = []
        self.dealer = Dealer()
        self.game_on = True
    def setup_players(self):
        """Function to setup the players names and quantity"""
        num_of_players = int(input("How many players are playing (1-4): "))
        for i in range (num_of_players):
            name = input(f"Enter the name for player {i+1}: ")
            player = Player.load_player_info(name)
            self.players.append(player)
    def take_bets(self):
        """Function that takes the bets of each player"""
        for player in self.players:
            slow_print(f"\n{player.name}'s balance: ${player.balance:.2f}")
            while True:
                try:
                    bet = float(input(
                    f"{player.name}, enter your wager ($1 - ${player.balance:.2f}): "
                                ))
                    if 1 <= bet <= player.balance:
                        player.wager = bet
                        break
                    slow_print(
                        "Invalid wager amount, please enter an amount greater than $1 "
                        "and that is within your balance."
                    )
                except ValueError:
                    continue
    def initialize_dealer(self):
        """Function that initializes dealers hand"""
        self.dealer.hand = []
        for player in self.players:
            player.reset_hand()
            player.hand.append(self.deck.pop())
        self.dealer.hand.append(self.deck.pop())
        for player in self.players:
            player.hand.append(self.deck.pop())
        self.dealer.hidden_card = self.deck.pop()
        slow_print(f"\nDealer shows: {self.dealer.hand[0].rank} of {self.dealer.hand[0].suit}")
    def player_turns(self):
        """Function that determines if the players busts or not and if they want to hit"""
        for player in self.players:
            while True:
                player_hand_value = hand_value(player.hand)
                slow_print(
                    f"\n{player.name}'s hand: "
                    f"{', '.join(f'{c.rank} of {c.suit}' for c in player.hand)} "
                    f"(Value: {player_hand_value})"
                    )
                if player_hand_value > 21:
                    slow_print(f"{player.name} busted!")
                    break
                if player_hand_value == 21:
                    slow_print(f"{player.name} has 21.")
                    break
                choice = input("Do you want to hit? (y/n): ").lower()
                if choice == 'y':
                    card = self.deck.pop()
                    slow_print(f"Dealt: {card.rank} of {card.suit}")
                    player.hand.append(card)
                elif choice == 'n':
                    break
                else:
                    slow_print("Invalid Choice. Please enter 'y' or 'n'.")
    def dealer_turn(self):
        """Function that determines if the dealer busts or not and if they hit"""
        slow_print("\nDealer Turn....")
        self.dealer.hand.append(self.dealer.hidden_card)
        dealer_value = hand_value(self.dealer.hand)
        slow_print(
            f"Dealer's hand: {', '.join(f'{c.rank} of {c.suit}' for c in self.dealer.hand)} "
            f"Value: {dealer_value}"
            )
        while dealer_value < 17 and any(hand_value(p.hand) <= 21 for p in self.players):
            time.sleep(1)
            card = self.deck.pop()
            self.dealer.hand.append(card)
            dealer_value = hand_value(self.dealer.hand)
            slow_print(f"Dealer hits: {card.rank} of {card.suit}")
        if dealer_value > 21:
            slow_print(f"Dealer busted with value: {dealer_value}")
        elif dealer_value <= 21:
            slow_print(f"Dealer stands with value: {dealer_value}")
        return dealer_value
    def win_or_lose_cond(self, dealer_value):
        """Function that determines if the player(s) win or if the dealer does."""
        for player in self.players:
            player_value = hand_value(player.hand)
            if player_value > 21:
                slow_print(f"{player.name} busted. Lost ${player.wager:.2f}.")
                player.balance -= player.wager
                slow_print(f"{player.name}'s Current Balance: {player.balance}")
            elif dealer_value > 21 or player_value > dealer_value:
                slow_print(f"{player.name} wins! Gains ${player.wager:.2f}.")
                player.balance += player.wager
                slow_print(f"{player.name}'s Current Balance: {player.balance}")
            elif player_value == dealer_value:
                slow_print(f"{player.name} pushes. No money was lost.")
                slow_print(f"{player.name}'s Current Balance: {player.balance}")
            else:
                slow_print(f"{player.name} loses. Lost ${player.wager:.2f}.")
                player.balance -= player.wager
                slow_print(f"{player.name}'s Current Balance: {player.balance}")
            if player.balance <= 0:
                slow_print(f"{player.name} is broke!")
                player.balance = 100.00
                slow_print(f"Sympathy money is given. {player.name} now has $100.00.")
        for player in self.players:
            player.wager = 0.00
            player.save_player_info()
    def run(self):
        """Function that runs the black jack game"""
        self.setup_players()
        while self.game_on:
            if len(self.deck) < self.cut_card_position:
                slow_print("Shuffling cards...")
                self.deck = FrenchDeck.create_deck()
                self.deck, self.cut_card_position = FrenchDeck.shuffle_and_cut_card(self.deck)
            self.take_bets()
            self.initialize_dealer()
            self.player_turns()
            dealer_value = self.dealer_turn()
            self.win_or_lose_cond(dealer_value)
            play_again = input("\nWould you like to play another round? (y/n): ").lower()
            if play_again != 'y':
                print("Thanks for playing!")
                self.game_on = False
            else:
                clear_console()
if __name__ == '__main__':
    BlackJackGame().run()
