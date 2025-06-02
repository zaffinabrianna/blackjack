#!/usr/bin/env python3
"""Main Code to run my BlackJackGame."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bjgame import game
from sys import exit
"""
Imports the bjgame and executes the main function.
"""
if __name__ == "__main__":
    exit(game.BlackJackGame().run())
