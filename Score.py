class Score:
    """
    A class for scoring the Go Fish Game

    Attributes
    ----------
    points_dict : dict
        Point values of individual cards

    Methods
    ----------
    calc(comp:list, user:list):
        Calculates the scores of the user hand and comp hand

    Reference
    ----------
    All code in GoFishGame.py, Deck.py, Player.py, Score.py is from
    Professor Jamshidi's go_fish.py file

    The code has minor changes to conform to Object Oriented
    Programming
    """

    # Attributes
    points_dict = { "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9,
                    "10":10, "J":11, "Q":12, "K":13, "A":14 }

    # Methods
    def __init__(self):  # not necessarily needed
        """
        Constructs the Score object
        """
        pass

    def calc(self, comp: list, user: list):
        """
        Scores players once game is over

        Parameters
        ----------
            comp : list
                Computer hand to be scored
            user : list
                User hand to be scored
        """

        comp_score = 0
        for card in set(comp):
            comp_score += self.points_dict[card]

        user_score = 0
        for card in set(user):
            user_score += self.points_dict[card]

        print("Your score is ", user_score)
        print("The computer's score is ", comp_score)

        if user_score > comp_score:
            print("You win! Well done!")
        elif user_score < comp_score:
            print("You lost. Better luck next time!")
        else:
            print("You tied! Good match!")
