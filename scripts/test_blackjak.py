import pytest
from project.scr.persons import BlackjackPlayer
from project.scr.objects import PlayingCard, PlayerHand, GameResult, CardSuit
from project.scr.strategies import ScientificStrategy, HighRiskStrategy
from project.scr.game import BlackjackGame, RoundPhase
from project.scr.desk import BlackjackTable

# Test card definitions
ACE = PlayingCard(CardSuit.SPADES, 'A')
KING = PlayingCard(CardSuit.HEARTS, 'K')
QUEEN = PlayingCard(CardSuit.DIAMONDS, 'Q')
JACK = PlayingCard(CardSuit.CLUBS, 'J')
TEN = PlayingCard(CardSuit.SPADES, '10')
NINE = PlayingCard(CardSuit.HEARTS, '9')
EIGHT = PlayingCard(CardSuit.DIAMONDS, '8')
SEVEN = PlayingCard(CardSuit.CLUBS, '7')
SIX = PlayingCard(CardSuit.SPADES, '6')
FIVE = PlayingCard(CardSuit.HEARTS, '5')
FOUR = PlayingCard(CardSuit.DIAMONDS, '4')
TWO = PlayingCard(CardSuit.CLUBS, '2')


@pytest.fixture
def test_players():
    """Fixture providing different player strategies for testing"""
    return [
        BlackjackPlayer(strategy=ScientificStrategy(), initial_bankroll=1000),
        BlackjackPlayer(strategy=HighRiskStrategy(), initial_bankroll=1000),
        BlackjackPlayer(strategy=ScientificStrategy(), initial_bankroll=1000),
        BlackjackPlayer(initial_bankroll=1000)
    ]


def test_game_phases(test_players):
    """Verify game progresses through all expected phases"""
    game = BlackjackGame(test_players)
    phases = []

    game.start_new_round()
    phases.append(game.current_phase)

    game.process_betting_phase()
    phases.append(game.current_phase)

    game.process_initial_deal()
    phases.append(game.current_phase)

    game.process_player_turns()
    phases.append(game.current_phase)

    game.process_dealer_turn()
    phases.append(game.current_phase)

    game.process_payouts()
    phases.append(game.current_phase)

    game.complete_round()
    phases.append(game.current_phase)

    assert phases == [
        RoundPhase.INITIALIZATION,
        RoundPhase.BETTING,
        RoundPhase.INITIAL_DEAL,
        RoundPhase.PLAYER_TURNS,
        RoundPhase.DEALER_TURN,
        RoundPhase.PAYOUTS,
        RoundPhase.COMPLETION
    ]


@pytest.mark.parametrize("cards,expected_score", [
    ([ACE, KING], 21),
    ([NINE, TEN], 19),
    ([ACE, ACE, NINE], 21),
    ([TEN, FIVE, SIX], 21),
    ([TEN, TEN, FIVE], -1),
    ([ACE, ACE, ACE, ACE], 14),
    ([JACK, QUEEN], 20)
])
def test_hand_scoring(cards, expected_score):
    """Test hand score calculation with various card combinations"""
    hand = PlayerHand(cards.copy())
    assert hand.calculate_value() == expected_score


def test_blackjack_detection():
    """Verify blackjack detection works correctly"""
    blackjack = PlayerHand([ACE, KING])
    not_blackjack1 = PlayerHand([NINE, TEN, TWO])
    not_blackjack2 = PlayerHand([ACE, FIVE, FIVE])

    assert blackjack.is_blackjack() is True
    assert not_blackjack1.is_blackjack() is False
    assert not_blackjack2.is_blackjack() is False


def test_bankroll_management(test_players):
    """Test player bankroll changes correctly during game"""
    game = BlackjackGame(test_players)
    initial_bankrolls = [p._bankroll for p in test_players]

    # Play full round
    game.play_full_round()

    # Verify bankroll changes
    for i, player in enumerate(test_players):
        if game.table.player_hands[player][0].status == GameResult.WIN:
            assert player._bankroll > initial_bankrolls[i]
        elif game.table.player_hands[player][0].status == GameResult.LOSE:
            assert player._bankroll < initial_bankrolls[i]
        elif game.table.player_hands[player][0].status == GameResult.PUSH:
            assert player._bankroll == initial_bankrolls[i]


