import random
import enum
"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

moves = ['rock', 'paper', 'scissors']
moves2 = ['rock', 'paper', 'scissors', 'spock', 'lizard']

"""The Player class is the parent class for all of the Players
in this game"""


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


def beats2(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock') or
            (one == 'rock' and two == 'lizard') or
            (one == 'lizard' and two == 'spock') or
            (one == 'spock' and two == 'rock') or
            (one == 'scissors' and two == 'lizard') or
            (one == 'lizard' and two == 'paper') or
            (one == 'paper' and two == 'spock') or
            (one == 'spock' and two == 'scissors'))


class Color(enum.Enum):
    red = '\033[91m'
    purple = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    black = '\033[0m'
    bold = '\033[1m'

    @classmethod
    def get_color(self, text_color):
        l_color = [color.value for color in self if color.name == text_color]
        return l_color[0]


class Player:
    times = 0

    def __init__(self, name=''):
        Player.times += 1
        self.score = 0
        self.my_move = ''
        self.their_move = ''
        if name == '':
            self.name = str(Player.times)
        else:
            self.name = name

    def move(self):
        return 'rock'

    def set_score(self, score):
        self.score += score

    def get_score(self):
        return self.score

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def learn(self, my_move, their_move):
        pass


class RandomPlayer(Player):
    def move(self):
        return random.choice(moves)


class ReflectPlayer(Player):
    def move(self):
        if self.their_move == '':
            self.my_move = random.choice(moves)
        else:
            self.my_move = self.their_move
        return self.my_move

    def learn(self, my_move, their_move):
        self.my_move = my_move
        self.their_move = their_move


class CyclePlayer(Player):
    def move(self):
        if self.my_move == '':
            self.my_move = random.choice(moves)
        else:
            self.location = moves.index(self.my_move)
            if self.location == len(moves) - 1:
                self.my_move = moves[0]
            else:
                self.my_move = moves[self.location + 1]
        return self.my_move

    def learn(self, my_move, their_move):
        self.my_move = my_move
        self.their_move = their_move


class HumanPlayer(Player):
    def move(self):
        print("('quit' to quit)")
        return self.valid_input(f'{", ".join(moves)}? > ', moves + ['quit'])

    def valid_input(self, prompt, options):
        while True:
            option = input(prompt).lower()
            if option in options:
                return option
            print(f'Sorry, the option "{option}" is invalid. Try again!')


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def winner(self):
        if self.p1.get_score() > self.p2.get_score():
            self.print_general("\nFinal Score: ** PLAYER "
                               f"({self.p1.get_name()}) WINS **")
        elif self.p2.get_score() > self.p1.get_score():
            self.print_general("\nFinal Score: ** PLAYER "
                               f"({self.p2.get_name()}) WINS **")
        else:
            self.print_general("\nFinal Score: ** TIE **")

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        if move1 == 'quit' or move2 == 'quit':
            return False
        print(f"You played {move1}.\nOpponent played {move2}.")
        if beats(move1, move2):
            self.p1.set_score(1)
            self.print_general(f"** PLAYER ({self.p1.get_name()}) WINS **")
        elif beats(move2, move1):
            self.p2.set_score(1)
            self.print_general(f"** PLAYER ({self.p2.get_name()}) WINS **")
        else:
            self.print_general("** TIE **")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)
        return True

    def print_general(self, text):
        print(Color.get_color('green')+text)
        print(f"Score: Player ({self.p1.get_name()}): {self.p1.get_score()},"
              f" Player ({self.p2.get_name()}): {self.p2.get_score()}")

    def play_single(self):
        print(Color.get_color('red')+"Game start!")
        print(Color.get_color('cyan')+"\nRound 1:")
        self.play_round()
        self.winner()
        print(Color.get_color('red')+"Game over!")

    def play_game(self):
        self.round = 0
        print(Color.get_color('red')+"Game start!")
        while True:
            self.round += 1
            print(Color.get_color('cyan')+f"\nRound {self.round}:")
            if not self.play_round():
                break
        self.winner()
        print(Color.get_color('red')+"Game over!")


if __name__ == '__main__':
    game = Game(HumanPlayer(), RandomPlayer())
    game.play_game()
