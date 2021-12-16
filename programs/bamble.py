import random


__doc__ = """
Bamble is a fun game you can play that allows you
to spend a currency called bamble bucks.

You have a 50/50 shot of winning or losing.
When you start the program you will by default
have 300 bamble bucks that you can use for voting.

[HOW TO PLAY]:
    It will first ask you how many bamble bucks you would
    like to vote. The minimum being 100 and the maximum being
    the amount of bamble bucks you already have.

    Once you finish entering the amount of bamble bucks to
    vote on the game. You then will either type 0 for heads, or 
    1 for tails. Then press enter to continue.

    After you typed the necessary data for the game, you will either
    gain the amount of bamble bucks entered or lose it. Once your
    bamble bucks hit 0, the program will stop.

[HOW TO START]:
    Run: python bamble.py

[MISSING FEATURES]:
    - Total Losses
    - Win Streak
    - Loss Streak
"""


class GameEngine:
    def __init__(self):
        self.bubbles = 300
        self.win_streak = 0
        self.total_wins = 0
        self.total_losses = 0

    def __valid_vote_amount(self, vote_amount):
        # Valid vote returns 1
        return (vote_amount <= self.bubbles) + 0

    def __call_vote(self, vote):
        output = random.randint(0, 1)
        return {"outcome": ((output == vote) + 0), "boolean_outcome": (output == vote)}

    def __update_bubbles(self, vote_amount, vote_outcome):
        calculated_amount = (self.__valid_vote_amount(vote_amount) * vote_outcome * vote_amount)
        self.bubbles += calculated_amount - (vote_amount * (calculated_amount == 0))

    def start(self):
        print("======================================\n")
        print("Vote!")
        user_vote_amount = int(input("Bubbles to Bamble: "))

        print("Heads(0) or Tails(1)?")
        user_vote = int(input(":"))
        vote_outcome = self.__call_vote(user_vote)

        self.total_wins += vote_outcome["outcome"]
        self.total_losses += abs(vote_outcome["boolean_outcome"] - 1)
        self.__update_bubbles(user_vote_amount, vote_outcome["outcome"])


def main():
    game = GameEngine()
    while not game.bubbles == 0:
        game.start()
        print(game.bubbles)
        print("\n======================================")
    print("Sorry! You're all out of Bamble Bucks :(")


if __name__ == '__main__':
    main()
