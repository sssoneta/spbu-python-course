from project.scr.persons import Player
from project.scr.strategies import Aggressive, Optimal1, Optimal2
from project.scr.game import Game


players = [
    Player(strategy=Optimal1()),
    Player(strategy=Optimal2()),
    Player(strategy=Aggressive()),
    Player(chips=15),
]
blackjack = Game(players)
blackjack.play_round_with_show_states()
blackjack.play_round_with_show_states()
