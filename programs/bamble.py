import random


with open("../documentation/bamble-doc.txt", "r") as DOC_FILE:
    __doc__ = DOC_FILE.read()


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
