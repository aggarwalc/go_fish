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
    def __init__(self):  # not necessarily needed
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
    def ask_user(self, comp: list, deck: object) -> str:
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

        while (invalid):

            print("What card would you like? ")

            resp = input("Enter one of your cards: " +
                         str(set(self.hand)) + ": ")
            resp = resp.upper()  # addition to check lower cases as well

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

        # return the requested card so that the computer can make use of this info
        return resp

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
    percept_sequence : list
        The past moves of the user
    comp_history : list
        The past 3 moves of the computer
    game_knowledge : dictionary
        Knowledge including deck length and user hand length

    Methods
    ----------
    ask_comp(user:list, deck:object):
        Computer requests a card from the user
    get_game_knowledge(self, user: list, deck: list, points: dict):
        Constructs the computer's game knowledge
    check_precept(self, cards: list) -> list:
        Filters the card list for cards that are in the precept sequence
    max_points(self, cards: list) -> str:
        Finds the card with the highest point value
    """

    # Attributes
    hand = []

    # past moves from the user
    percept_sequence = []
    # past (3) moves from the computer
    comp_history = [None, None, None]
    # computer's game knowledge
    # will contain (user hand length, deck length, percept, comp_history, scoring_guide)
    game_knowledge = {}

    def ask_comp(self, user: list, gamedeck: object):
        """
        Computer requests a card from the user

        Parameters
        ----------
            user : list
                The user's hand
            gamedeck : object
                The gamedeck in use
        """

        # possible moves - actions
        # fundamentally, the bot can ask for any card as long as it exists in
        # the computer's hand. But we want to narrow this list down to contain the
        # best cards to ask for.

        # card_counts contains the counts of cards that do not have full books and
        # have not been asked for in the past three moves
        card_counts = {card: self.hand.count(card) for card in self.hand if (
            self.hand.count(card) != 4 and card not in self.game_knowledge['comp_history'])}

        if len(card_counts) == 0:
            resp = self.hand[randint(0, len(self.hand) - 1)]
            print(resp)
        else:
            # BOT -
            # Step 1: The bot will first go through the cards and prioritize the cards that
            # have the largest count below 4
            # Step 2: The bot will then filter this list of cards further and prioritize cards
            # that have been asked for before by the user
            # Step 3: Finally, If there are still multiple cards in the list, the bot will choose
            # the one with the highest point value to maximize computer's score [performance measure]

            # find the max count of cards
            max_count = max(card_counts.values())

            # add all the cards that have the max count to potential_cards list
            potential_cards = [
                card for card in card_counts if card_counts[card] == max_count]

            # check if the cards in potential_card have been asked for before
            # if they have, then we want to keep them in the list
            # if they haven't remove them from the list
            potential_cards = self.check_precept(potential_cards)

            # if there are still multiple cards in potential_cards
            # pick the one with the highest point value
            resp = self.max_points(potential_cards)

        print("The computer is requesting", resp)
        input("Press enter to continue.")

        if resp in user:
            print("You have this card")
            self.give_cards(user, self.hand, resp)
        else:
            print("You do not have card")
            self.go_fish(self.hand, gamedeck)
            print("The computer has drawn a card.")

        # alter comp_history so that it only has the three past moves at all times
        self.comp_history.pop(0)
        self.comp_history.append(resp)

    def get_game_knowledge(self, user: list, deck: list, points: dict):
        """
        Constructs the computer's game knowledge

        Parameters
        ----------
            user : list
                The user's hand
            deck : list
                The deck in use
            points : dict
                Point values of individual cards
        """

        # add information to game knowledge dictionary
        self.game_knowledge['user_hand_len'] = len(user)
        self.game_knowledge['deck_len'] = len(deck)
        self.game_knowledge['percept'] = self.percept_sequence
        self.game_knowledge['comp_history'] = self.comp_history
        self.game_knowledge['scoring_guide'] = points

    def check_precept(self, cards: list) -> list:
        """
        Checks if any of the cards have previously been asked for by the user

        Parameters
        ----------
            cards : list
                A list of possible cards that the computer can ask for
        """
        filtered_cards = []
        for card in cards:
            # check if card is in the precept sequence
            if card in self.game_knowledge['percept']:
                filtered_cards.append(card)

        # if none of the cards were asked for before, return the original list
        # otherwise, return the filtered list
        if len(filtered_cards) == 0:
            return cards
        else:
            return filtered_cards

    def max_points(self, cards: list) -> str:
        """
        Finds the card with the highest point value

        Parameters
        ----------
            cards : list
                A list of possible cards that the computer can ask for
        """
        max_point_card = None
        # compare point values of cards based on the scoring guide
        for card in cards:
            if max_point_card == None:
                max_point_card = card
            elif self.game_knowledge['scoring_guide'][card] > self.game_knowledge['scoring_guide'][max_point_card]:
                max_point_card = card

        return max_point_card
