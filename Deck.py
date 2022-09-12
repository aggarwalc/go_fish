from random import randint

class Deck:
    """
    A class for the gamedeck in the Go Fish Game

    Attributes
    ----------
    cards : list
        The thirteen possible cards of a deck
    deck : list
        A complete deck of cards

    Methods
    ----------
    draw_card() -> str:
        Draws a card from the gamedeck
    deal_cards(user:list, comp:list):
        Deals cards to both players (user and computer)

    Reference
    ----------
    All code in GoFishGame.py, Deck.py, Player.py, Score.py is from
    Professor Jamshidi's go_fish.py file

    The code has minor changes to conform to Object Oriented
    Programming
    """
    # Attributes
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = cards*4

    # Methods
    def __init__(self):  # not necessarily needed
        """
        Constructs the Deck object
        """
        pass

    def draw_card(self) -> str:
        """
        Draws a single card and removes it from deck
        """

        if len(self.deck) > 0:
            card = self.deck[randint(0, len(self.deck)-1)]
            self.deck.remove(card)
            return card
        else:
            print("Deck is out of cards")
            return None

    def deal_cards(self, user: list, comp: list):
        """
        Deals cards for user and computer

        Parameters
        ----------
            user : list
                The user's hand
            comp : list
                The computer's hand
        """

        for i in range(7):
            user.append(self.draw_card())
            comp.append(self.draw_card())

        user.sort()
