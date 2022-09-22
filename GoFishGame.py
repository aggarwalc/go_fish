# RUN THIS FILE TO PLAY GAME
from Score import *
from Player import *
from Deck import *


class GoFishGame:
    """
    A class for the Go Fish card game

    Attributes
    ----------
    score : object
        Instance of the Score class
    user : object
        Instance of the User class
    comp : object
        Instance of the Comp class
    gamedeck : object
        Instance of the Deck class

    Methods
    ----------
    play_again() -> bool:
        Return True if user wishes to play again
    is_game_over() -> bool:
        Return True if the game has finished
    play():
        Runs a full game of Go Fish

    Reference
    ----------
    All code in GoFishGame.py, Deck.py, Player.py, Score.py is from
    Professor Jamshidi's go_fish.py file

    The code has minor changes to conform to Object Oriented
    Programming
    """

    # Attributes
    score = Score()
    user = User()
    comp = Comp()
    gamedeck = Deck()

    # Methods
    def __init__(self):
        """
        Constructs the GoFishGame object and greets the user
        """

        # welcome message
        print("Welcome to the game 'Go Fish'!")
        print("Your goal is to collect as many ")
        print("4-of-a-kind, or 'books', as you can.")
        print("Books are scored based on the card ")
        print("value with Aces being the highest and ")
        print("'2' being the lowest. Now let's play! Good luck!")
        input("Press enter to continue")

    def is_game_over(self):
        """
        Determines if game is over
        """
        # check that deck is empty ?
        if len(self.gamedeck.deck) > 0:
            return False

        for card in set(self.comp.hand):
            count = self.comp.hand.count(card)
            if count != 4:
                return False

        for card in set(self.user.hand):
            count = self.user.hand.count(card)
            if count != 4:
                return False

        return True

    def play_again(self) -> bool:
        """
        Prompts user if they wish to play again
        """

        while (True):

            resp = input("Would you like to play again? (Y/N): ")
            resp = resp.upper()

            if resp == "Y":
                self.user.hand.clear()
                self.comp.hand.clear()

                # reset precept_sequence and comp_history
                self.comp.percept_sequence.clear()
                self.comp_history = [None, None, None]

                for card in self.gamedeck.cards:
                    for i in range(4):
                        self.gamedeck.deck.append(card)

                return True

            if resp == "N":
                return False

            print("Invalid input")

    def play(self):
        """
        Runs a full game of Go Fish
        """

        # deals cards to user and computer
        self.gamedeck.deal_cards(self.user.hand, self.comp.hand)
        # main gameplay
        while (not self.is_game_over()):
            req = self.user.ask_user(self.comp.hand, self.gamedeck)
            # add request to computer's percept sequence
            self.comp.percept_sequence.append(req)
            if self.is_game_over():
                break
            input("Press enter to continue")
            # construct coputer's game knowledge
            self.comp.get_game_knowledge(
                self.user.hand, self.gamedeck.deck, self.score.points_dict)
            self.comp.ask_comp(self.user.hand, self.gamedeck)
            input("Press enter to continue")
            self.user.display(self.comp.hand)
        # finish game, calculate score
        print("The game is over!")
        self.score.calc(self.comp.hand, self.user.hand)
        if self.play_again():
            new_game = GoFishGame()
            new_game.play()


# main
if __name__ == "__main__":
    game = GoFishGame()
    game.play()
