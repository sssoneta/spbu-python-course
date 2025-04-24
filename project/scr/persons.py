from typing import List
import random
from project.scr.objects import CardDeck, PlayerHand, PlayingCard
from project.scr.strategies import BaseStrategy, ConservativeStrategy


class BlackjackPlayer:
    """
    Represents a player in blackjack game with betting capabilities and strategy.

    Attributes:
        strategy (BaseStrategy): The playing strategy to use
        bankroll (int): Current chip count
        current_bet (int): Active wager amount
    """

    def __init__(self, strategy: BaseStrategy = None, initial_bankroll: int = 1000):
        self.strategy = strategy or ConservativeStrategy()
        self._bankroll = initial_bankroll
        self.current_bet = 0
        self.active_hands: List[PlayerHand] = []

    def adjust_bankroll(self, amount: int) -> None:
        """Modify player's chip count by specified amount"""
        self._bankroll += amount

    def can_place_bet(self, amount: int) -> bool:
        """Check if player has sufficient funds for a bet"""
        return 0 < amount <= self._bankroll

    def place_bet(self, amount: int) -> bool:
        """Attempt to place a wager, returns True if successful"""
        if self.can_place_bet(amount):
            self.current_bet = amount
            self._bankroll -= amount
            return True
        return False

    def clear_hands(self) -> None:
        """Reset all active hands for new round"""
        self.active_hands = []

    def add_hand(self, hand: PlayerHand) -> None:
        """Add a new hand to player's active hands"""
        self.active_hands.append(hand)


class BlackjackDealer:
    """
    Manages the dealer's operations including card dealing and game flow.

    Attributes:
        shoe (List[CardDeck]): Collection of card decks in play
        hand (PlayerHand): Dealer's current hand
    """

    def __init__(self, deck_count: int = 6):
        self.shoe = self._initialize_shoe(deck_count)
        self.hand: PlayerHand = None

    def _initialize_shoe(self, deck_count: int) -> List[CardDeck]:
        """Create and shuffle multiple decks for the shoe"""
        decks = [CardDeck() for _ in range(deck_count)]
        for deck in decks:
            deck.shuffle_cards()
        return decks

    def deal_card(self, face_up: bool = True) -> PlayingCard:
        """
        Deal a card from random deck in shoe

        Args:
            face_up: Whether card should be dealt face up

        Returns:
            PlayingCard: The dealt card
        """
        active_deck = random.choice(self.shoe)
        try:
            card = active_deck.deal_card()
            card.face_up = face_up
            return card
        except ValueError:
            # Reshuffle if deck is empty
            self.shoe = self._initialize_shoe(len(self.shoe))
            return self.deal_card(face_up)

    def reveal_hand(self) -> None:
        """Show dealer's hand with all cards face up"""
        if self.hand:
            for card in self.hand.cards:
                card.face_up = True
            print("\nDealer's Hand:")
            self.hand.display()

    def new_round(self) -> None:
        """Prepare dealer for new game round"""
        self.hand = PlayerHand([])
        # Check if shoe needs replenishing
        if sum(deck.remaining for deck in self.shoe) < 52:
            self.shoe = self._initialize_shoe(len(self.shoe))
