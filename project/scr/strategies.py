from enum import Enum, auto
from typing import Optional
from dataclasses import dataclass
from project.scr.objects import PlayerHand, PlayingCard


class PlayerAction(Enum):
    """Defines possible actions a player can take in blackjack"""

    STAND = auto()
    HIT = auto()
    SPLIT = auto()
    DOUBLE = auto()
    TRIPLE = auto()
    SURRENDER = auto()


@dataclass
class BaseStrategy:
    """Abstract base class for all blackjack strategies"""

    min_bet: int = 10
    use_insurance: bool = False

    def decide_action(
        self, hand: PlayerHand, dealer_upcard: PlayingCard
    ) -> PlayerAction:
        """Determine optimal action based on game state"""
        raise NotImplementedError("Strategy subclass must implement decide_action")


class ConservativeStrategy(BaseStrategy):
    """Basic strategy with minimal risk"""

    def __init__(self):
        super().__init__(use_insurance=True)

    def decide_action(
        self, hand: PlayerHand, dealer_upcard: PlayingCard
    ) -> PlayerAction:
        hand_value = hand.calculate_value()

        if hand_value < 17:
            return PlayerAction.HIT
        return PlayerAction.STAND


class ScientificStrategy(BaseStrategy):
    """Mathematically optimal strategy based on probability"""

    def decide_action(
        self, hand: PlayerHand, dealer_upcard: PlayingCard
    ) -> PlayerAction:
        cards = hand.cards
        hand_value = hand.calculate_value()
        dealer_rank = dealer_upcard.rank

        # Check for split opportunities first
        split_action = self._evaluate_split(cards, dealer_rank)
        if split_action:
            return split_action

        # Check for double down opportunities
        double_action = self._evaluate_double(hand_value, dealer_rank)
        if double_action and len(cards) == 2:
            return double_action

        # Handle soft totals (ace counted as 11)
        if self._is_soft_hand(cards):
            return self._handle_soft_hand(hand_value - 10, dealer_rank)

        # Standard decision making
        return self._handle_hard_hand(hand_value, dealer_rank)

    def _evaluate_split(
        self, cards: list[PlayingCard], dealer_rank: str
    ) -> Optional[PlayerAction]:
        if len(cards) != 2 or cards[0].rank != cards[1].rank:
            return None

        card_rank = cards[0].rank
        if card_rank in ("A", "8"):
            return PlayerAction.SPLIT if dealer_rank != "A" else PlayerAction.HIT
        elif card_rank == "5":
            return PlayerAction.DOUBLE
        elif card_rank in ("2", "3", "7"):
            return (
                PlayerAction.SPLIT
                if dealer_rank in ("2", "3", "4", "5", "6", "7")
                else PlayerAction.HIT
            )
        elif card_rank in ("4", "6", "9"):
            # Additional split logic for these ranks
            pass

        return None

    def _evaluate_double(
        self, hand_value: int, dealer_rank: str
    ) -> Optional[PlayerAction]:
        if hand_value == 9 and dealer_rank in ("2", "3", "4", "5", "6"):
            return PlayerAction.DOUBLE
        elif hand_value in (10, 11) and dealer_rank not in ("A", "10", "J", "Q", "K"):
            return PlayerAction.DOUBLE
        return None

    def _is_soft_hand(self, cards: list[PlayingCard]) -> bool:
        return (
            any(card.rank == "A" for card in cards)
            and sum(
                11
                if card.rank == "A"
                else 10
                if card.rank in ("J", "Q", "K")
                else int(card.rank)
                for card in cards
            )
            <= 21
        )

    def _handle_soft_hand(self, hand_value: int, dealer_rank: str) -> PlayerAction:
        if hand_value <= 7:
            return (
                PlayerAction.HIT
                if dealer_rank in ("9", "10", "J", "Q", "K", "A")
                else PlayerAction.DOUBLE
            )
        elif hand_value == 8:
            return (
                PlayerAction.STAND
                if dealer_rank in ("2", "3", "4", "5", "6")
                else PlayerAction.HIT
            )
        else:
            return PlayerAction.STAND

    def _handle_hard_hand(self, hand_value: int, dealer_rank: str) -> PlayerAction:
        if hand_value <= 11:
            return PlayerAction.HIT
        elif 12 <= hand_value <= 16:
            return (
                PlayerAction.STAND
                if dealer_rank in ("2", "3", "4", "5", "6")
                else PlayerAction.HIT
            )
        else:
            return PlayerAction.STAND


class HighRiskStrategy(BaseStrategy):
    """Aggressive betting strategy with higher risk/reward"""

    def __init__(self):
        super().__init__(min_bet=20)

    def decide_action(
        self, hand: PlayerHand, dealer_upcard: PlayingCard
    ) -> PlayerAction:
        hand_value = hand.calculate_value()

        if hand_value <= 6:
            return PlayerAction.DOUBLE
        elif hand_value <= 15:
            return PlayerAction.HIT
        else:
            return PlayerAction.STAND
