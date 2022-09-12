from random import randint
from Deck import *

class Player:
    """
    A parent class for players of the Go Fish Game

    Methods
    ----------
    go_fish(hand:list, deck:object) -> str:
        Prints go fish and draws a card from the deck
    give_cards(giver: list, taker: list, card: str) -> tuple:
        Transfers cards from one player to another

    Reference
    ----------
    All code in GoFishGame.py, Deck.py, Player.py, Score.py is from
    Professor Jamshidi's go_fish.py file

    The code has minor changes to conform to Object Oriented
    Programming
    """

    # Methods
    def __init__(self): # not necessarily needed
        """
        Constructs the Player object
        """
        pass

    def go_fish(self, hand: list, deck: object) -> str:
        """
        Prints go fish and draws a card

        Parameters
        ----------
            hand : list
                The Hand to which a card will be added
            deck : object
                The deck to draw a card from
        """

        print("Go fish!")
        card = deck.draw_card()

        hand.append(card)
        hand.sort()

        return card

    def give_cards(self, giver: list, taker: list, card: str) -> tuple:
        """
        Passes cards from one hand to another

        Parameters
        ----------
            giver : list
                The giver's hand
            taker : list
                The recpient's hand
            card : str
                The card to be transferred
        """

        print("Transfering card " + card)

        while (card in giver):
            giver.remove(card)
            taker.append(card)

        taker.sort()

        return giver, taker


class User(Player):
    """
    A child class for the user player

    Attributes
    ----------
    hand : list
        The user's hand

    Methods
    ----------
    ask_user(comp:list, deck:object):
        Prompts the user to request a card
    display(comp:list):
        Displays the user's hand and information about the computer's hand
    """

    # Attributes
    hand = []

    # Methods
    def ask_user(self, comp: list, deck: object):
        """
        Asks the user to request a card

        Parameters
        ----------
            comp : list
                The computer's hand
            deck : object
                The gamedeck in use
        """

        invalid = True

        while(invalid):

            print("What card would you like? ")

            resp = input("Enter one of your cards: " + str(set(self.hand)) + ": ")
            resp = resp.upper() #addition to check lower cases as well

            if resp in self.hand:
                invalid = False
            else:
                print("Invalid response")

        if resp in comp:
            print("Computer has card")
            self.give_cards(comp, self.hand, resp)
        else:
            print("Computer does not have card")
            card = self.go_fish(self.hand, deck)
            print("Now adding " + card + " to you hand.")

    def display(self, comp: list):
        """
        Displays the contents of the hands

        Parameters
        ----------
            comp : list
                The computers's hand
        """

        print("The computer has", len(comp), "cards.")
        print("Your cards are: ")

        card_counts = []
        for card in set(self.hand):
            card_counts.append((self.hand.count(card), card))
        card_counts.sort(reverse=True)
        for pair in card_counts:
            print(pair[1], ":", pair[0])

class Comp(Player):
    """
    A child class for the computer player

    Attributes
    ----------
    hand : list
        The computer's hand

    Methods
    ----------
    ask_comp(user:list, deck:object):
        Computer requests a card from the user
    """

    # Attributes
    hand = []

    # Methods
    def ask_comp(self, user: list, deck: object):
        """
        Computer requests a card from the user

        Parameters
        ----------
            user : list
                The user's hand
            deck : object
                The gamedeck in use
        """

        potential_cards = []
        for card in set(self.hand):
            count = self.hand.count(card)
            if count != 4:
                potential_cards.append(card)

        if (len(potential_cards) > 0):
            index = randint(0, len(potential_cards) - 1)
            resp = potential_cards[index]
        else:
            # the computer has only books!
            resp = self.hand[randint(0, len(self.hand) - 1)]


        print("The computer is requesting", resp)
        input("Press enter to continue.")

        if resp in user:
            print("You have this card")
            self.give_cards(user, self.hand, resp)
        else:
            print("You do not have card")
            self.go_fish(self.hand, deck)
            print("The computer has drawn a card.")
