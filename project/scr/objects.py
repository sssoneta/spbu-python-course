from random import SystemRandom
from itertools import product
from enum import Enum, auto
from typing import List, Dict, Tuple, Optional, Union
from dataclasses import dataclass


class CardSuit(Enum):
    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()

    def __str__(self):
        return {
            CardSuit.CLUBS: "♣",
            CardSuit.DIAMONDS: "♦",
            CardSuit.HEARTS: "♥",
            CardSuit.SPADES: "♠",
        }[self]


class PlayingCard:
    """Represents a single playing card with suit and rank"""

    def __init__(self, suit: CardSuit, rank: Union[int, str]):
        self._suit = suit
        self._rank = str(rank).upper()

    @property
    def suit(self) -> CardSuit:
        return self._suit

    @property
    def rank(self) -> str:
        return self._rank

    def __repr__(self) -> str:
        return f"{self.rank}{str(self.suit)}"

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit.name.capitalize()}"


class CardDeck:
    """Implements a standard 52-card deck with advanced features"""

    def __init__(self, num_decks: int = 1):
        self._rng = SystemRandom()
        self._cards = self._initialize_deck(num_decks)
        self.shuffle_cards()

    def _initialize_deck(self, num_decks: int) -> List[PlayingCard]:
        ranks = [str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]
        return [
            PlayingCard(suit, rank)
            for _ in range(num_decks)
            for suit, rank in product(CardSuit, ranks)
        ]

    def shuffle_cards(self) -> None:
        """Performs cryptographic-quality shuffle"""
        self._rng.shuffle(self._cards)

    def deal_card(self) -> PlayingCard:
        """Removes and returns the top card from deck"""
        if not self._cards:
            raise ValueError("No cards remaining in deck")
        return self._cards.pop()

    @property
    def remaining(self) -> int:
        return len(self._cards)


class GameResult(Enum):
    ACTIVE = auto()
    WIN = auto()
    LOSE = auto()
    BLACKJACK = auto()
    PUSH = auto()
    BUST = auto()


@dataclass
class PlayerHand:
    cards: List[PlayingCard]
    wager: int = 0
    is_active: bool = True
    status: GameResult = GameResult.ACTIVE

    def add_card(self, card: PlayingCard) -> None:
        self.cards.append(card)

    def calculate_value(self) -> int:
        total = 0
        aces = 0

        for card in self.cards:
            if card.rank.isdigit():
                total += int(card.rank)
            elif card.rank in ("J", "Q", "K"):
                total += 10
            else:  # Ace
                total += 11
                aces += 1

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total if total <= 21 else -1

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.calculate_value() == 21

    def double_wager(self) -> None:
        self.wager *= 2

    def surrender(self) -> None:
        self.is_active = False
        self.status = GameResult.LOSE

    def split_hand(self) -> Tuple["PlayerHand", "PlayerHand"]:
        if len(self.cards) != 2:
            raise ValueError("Can only split with exactly two cards")

        hand1 = PlayerHand([self.cards[0]], self.wager)
        hand2 = PlayerHand([self.cards[1]], self.wager)
        return hand1, hand2

    def display(self) -> None:
        print("Current hand:")
        for card in self.cards:
            print(f"  {card}")
        print(f"Total value: {self.calculate_value()}")
