from project.scr.persons import BlackjackPlayer
from project.scr.strategies import ConservativeStrategy
from project.scr.game import BlackjackGame

# Минимальный рабочий пример с одной стратегией
players = [
    BlackjackPlayer(strategy=ConservativeStrategy(), initial_bankroll=100),
    BlackjackPlayer(initial_bankroll=100)  # Использует Conservative по умолчанию
]

game = BlackjackGame(players=players, num_decks=1)  # 1 колода для простоты
game.play_full_round()