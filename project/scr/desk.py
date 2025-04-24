from typing import List, Dict
from project.scr.persons import BlackjackPlayer, BlackjackDealer
from project.scr.objects import PlayerHand


class BlackjackTable:
    """
    Manages the blackjack game flow, player actions, and dealer interactions.

    Attributes:
        players (List[BlackjackPlayer]): List of active players
        dealer (BlackjackDealer): The game dealer
        player_hands (Dict[BlackjackPlayer, List[PlayerHand]]): Active hands per player
    """

    def __init__(self, players: List[BlackjackPlayer], num_decks: int = 6):
        """Initialize a new blackjack table"""
        self.players = players
        self.dealer = BlackjackDealer(num_decks)
        self.player_hands: Dict[BlackjackPlayer, List[PlayerHand]] = {}
        self._initialize_table()

    def _initialize_table(self) -> None:
        """Prepare the table for a new round"""
        self.dealer.new_round()
        for player in self.players:
            player.clear_hands()
            new_hand = PlayerHand([])
            player.add_hand(new_hand)
            self.player_hands[player] = [new_hand]

    def deal_card_to_hand(self, hand: PlayerHand, face_up: bool = True) -> None:
        """
        Deal a card from the dealer's shoe to a specific hand

        Args:
            hand: The target hand to receive the card
            face_up: Whether the card should be dealt face up
        """
        card = self.dealer.deal_card(face_up)
        hand.add_card(card)

    def place_initial_bets(self) -> None:
        """Handle initial betting round for all players"""
        for player in self.players:
            if player.can_place_bet(player.strategy.min_bet):
                bet_amount = player.strategy.min_bet
                player.place_bet(bet_amount)
                # Initialize bet for first hand
                if self.player_hands[player]:
                    self.player_hands[player][0].wager = bet_amount
            else:
                # Mark player as out if can't place minimum bet
                if self.player_hands[player]:
                    self.player_hands[player][0].status = GameResult.LOSE

    def split_hand(self, player: BlackjackPlayer, hand_index: int = 0) -> None:
        """
        Split a player's hand into two separate hands

        Args:
            player: The player requesting the split
            hand_index: Index of the hand to split
        """
        if hand_index >= len(self.player_hands[player]):
            return

        original_hand = self.player_hands[player][hand_index]

        # Verify split is possible
        if len(original_hand.cards) != 2 or \
                original_hand.cards[0].rank != original_hand.cards[1].rank:
            return

        # Create two new hands from the split
        new_hand1, new_hand2 = original_hand.split_hand()

        # Place additional bet
        if player.can_place_bet(original_hand.wager):
            player.place_bet(original_hand.wager)
        else:
            return

        # Deal cards to new hands
        self.deal_card_to_hand(new_hand1)
        self.deal_card_to_hand(new_hand2)

        # Replace original hand with split hands
        self.player_hands[player].pop(hand_index)
        self.player_hands[player].extend([new_hand1, new_hand2])
        player.active_hands = self.player_hands[player]

    def start_new_round(self) -> None:
        """Reset the table for a new round of play"""
        self._initialize_table()

        # Deal initial cards: 2 to each player, 1 to dealer + 1 face down
        for _ in range(2):
            for player in self.players:
                for hand in self.player_hands[player]:
                    self.deal_card_to_hand(hand)

        # Dealer gets one face up and one face down card
        self.deal_card_to_hand(self.dealer.hand)
        self.deal_card_to_hand(self.dealer.hand, face_up=False)

    def player_action(self, player: BlackjackPlayer, action: str, hand_index: int = 0) -> None:
        """
        Process player action for specific hand

        Args:
            player: The player taking action
            action: Action to perform (hit, stand, double, split, etc.)
            hand_index: Index of the hand to act upon
        """
        if hand_index >= len(self.player_hands[player]):
            return

        current_hand = self.player_hands[player][hand_index]

        match action:
            case "hit":
                self.deal_card_to_hand(current_hand)
                if current_hand.calculate_value() == -1:  # Bust
                    current_hand.status = GameResult.BUST

            case "stand":
                current_hand.status = GameResult.ACTIVE

            case "double":
                if player.can_place_bet(current_hand.wager):
                    player.place_bet(current_hand.wager)
                    current_hand.double_wager()
                    self.deal_card_to_hand(current_hand)
                    current_hand.status = GameResult.ACTIVE

            case "split":
                self.split_hand(player, hand_index)

            case "surrender":
                player.adjust_bankroll(current_hand.wager // 2)
                current_hand.surrender()