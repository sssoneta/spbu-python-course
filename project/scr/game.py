from enum import Enum, auto
from typing import List, Dict
from project.scr.objects import PlayerHand, PlayingCard, GameResult
from project.scr.persons import BlackjackPlayer, BlackjackDealer
from project.scr.strategies import PlayerAction, BaseStrategy
from project.scr.desk import BlackjackTable


class RoundPhase(Enum):
    """Represents different phases of a blackjack round"""

    INITIALIZATION = auto()
    BETTING = auto()
    INITIAL_DEAL = auto()
    PLAYER_TURNS = auto()
    DEALER_TURN = auto()
    PAYOUTS = auto()
    COMPLETION = auto()


class BlackjackGame:
    """
    Controls the flow of a blackjack game with multiple players and rounds.

    Attributes:
        table (BlackjackTable): The game table with players and dealer
        current_phase (RoundPhase): Current game phase
        round_number (int): Current round count
    """

    def __init__(self, players: List[BlackjackPlayer], num_decks: int = 6):
        """Initialize a new blackjack game session"""
        self.table = BlackjackTable(players, num_decks)
        self.current_phase = RoundPhase.INITIALIZATION
        self.round_number = 0
        self._setup_observers()

    def _setup_observers(self) -> None:
        """Setup game state observers for UI updates"""
        self.observers: list = []

    def _notify_observers(self) -> None:
        """Notify all observers about game state changes"""
        for observer in self.observers:
            observer.update(self)

    def start_new_round(self) -> None:
        """Begin a new round of blackjack"""
        self.round_number += 1
        self.current_phase = RoundPhase.INITIALIZATION
        self.table.start_new_round()
        self._notify_observers()

    def process_betting_phase(self) -> None:
        """Handle the betting phase of the round"""
        self.current_phase = RoundPhase.BETTING
        self.table.place_initial_bets()
        self._notify_observers()

    def process_initial_deal(self) -> None:
        """Perform the initial card deal"""
        self.current_phase = RoundPhase.INITIAL_DEAL
        self._notify_observers()

    def process_player_turns(self) -> None:
        """Handle all player decisions"""
        self.current_phase = RoundPhase.PLAYER_TURNS
        dealer_upcard = self.table.dealer.hand.cards[0]

        for player in self.table.players:
            for i, hand in enumerate(self.table.player_hands[player]):
                if hand.status != GameResult.ACTIVE:
                    continue

                while True:
                    action = player.strategy.decide_action(hand, dealer_upcard)

                    if action == PlayerAction.STAND:
                        break

                    elif action == PlayerAction.HIT:
                        self.table.deal_card_to_hand(hand)
                        if hand.calculate_value() == -1:  # Bust
                            hand.status = GameResult.BUST
                            break

                    elif action == PlayerAction.DOUBLE:
                        if len(hand.cards) == 2 and player.can_place_bet(hand.wager):
                            player.place_bet(hand.wager)
                            hand.double_wager()
                            self.table.deal_card_to_hand(hand)
                            break

                    elif action == PlayerAction.SPLIT:
                        if (
                            len(hand.cards) == 2
                            and hand.cards[0].rank == hand.cards[1].rank
                        ):
                            self.table.split_hand(player, i)
                            # Need to re-evaluate after split
                            continue

                    elif action == PlayerAction.SURRENDER:
                        if len(hand.cards) == 2:
                            player.adjust_bankroll(hand.wager // 2)
                            hand.status = GameResult.LOSE
                            break
        self._notify_observers()

    def process_dealer_turn(self) -> None:
        """Handle the dealer's play"""
        self.current_phase = RoundPhase.DEALER_TURN
        dealer_hand = self.table.dealer.hand

        # Dealer draws according to rules
        while dealer_hand.calculate_value() not in (-1, 17, 18, 19, 20, 21):
            self.table.deal_card_to_hand(dealer_hand)

        dealer_hand.status = (
            GameResult.WIN if dealer_hand.calculate_value() != -1 else GameResult.BUST
        )
        self._notify_observers()

    def process_payouts(self) -> None:
        """Calculate and distribute winnings"""
        self.current_phase = RoundPhase.PAYOUTS
        dealer_value = self.table.dealer.hand.calculate_value()
        dealer_busted = dealer_value == -1

        for player in self.table.players:
            for hand in self.table.player_hands[player]:
                if hand.status != GameResult.ACTIVE:
                    continue

                player_value = hand.calculate_value()

                if player_value == -1:  # Player busted
                    hand.status = GameResult.BUST

                elif len(hand.cards) == 2 and player_value == 21:  # Blackjack
                    hand.status = GameResult.BLACKJACK
                    player.adjust_bankroll(int(hand.wager * 2.5))

                elif dealer_busted or player_value > dealer_value:
                    hand.status = GameResult.WIN
                    player.adjust_bankroll(hand.wager * 2)

                elif player_value == dealer_value:
                    hand.status = GameResult.PUSH
                    player.adjust_bankroll(hand.wager)

                else:
                    hand.status = GameResult.LOSE
        self._notify_observers()

    def complete_round(self) -> None:
        """Clean up after round completion"""
        self.current_phase = RoundPhase.COMPLETION
        self._notify_observers()

    def play_full_round(self) -> None:
        """Execute a complete round from start to finish"""
        self.start_new_round()
        self.process_betting_phase()
        self.process_initial_deal()
        self.process_player_turns()
        self.process_dealer_turn()
        self.process_payouts()
        self.complete_round()

    def add_observer(self, observer) -> None:
        """Add a game state observer"""
        self.observers.append(observer)


class GameObserver:
    """Base class for game state observers"""

    def update(self, game: BlackjackGame) -> None:
        """Handle game state updates"""
        self._display_round_info(game)
        self._display_phase_info(game.current_phase)
        self._display_table_state(game.table)

    def _display_round_info(self, game: BlackjackGame) -> None:
        print(f"\n=== Round {game.round_number} ===")

    def _display_phase_info(self, phase: RoundPhase) -> None:
        phase_descriptions = {
            RoundPhase.INITIALIZATION: "Setting up new round...",
            RoundPhase.BETTING: "Players placing bets...",
            RoundPhase.INITIAL_DEAL: "Dealing initial cards...",
            RoundPhase.PLAYER_TURNS: "Players making decisions...",
            RoundPhase.DEALER_TURN: "Dealer playing hand...",
            RoundPhase.PAYOUTS: "Calculating results...",
            RoundPhase.COMPLETION: "Round complete!",
        }
        print(phase_descriptions.get(phase, ""))

    def _display_table_state(self, table: BlackjackTable) -> None:
        # Display dealer's hand
        print("\nDealer's Hand:")
        table.dealer.hand.display()

        # Display each player's hands
        for i, player in enumerate(table.players):
            print(f"\nPlayer {i + 1} (Bankroll: {player._bankroll}):")
            for j, hand in enumerate(table.player_hands[player]):
                print(f"  Hand {j + 1} (Bet: {hand.wager}):")
                hand.display()
                print(f"  Status: {hand.status.name}")
