import random

# Define card ranks and their corresponding numerical values
CARD_RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
CARD_VALUES = {
    'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13
}
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

def create_deck():
    """Creates a standard 52-card deck represented as (rank, value) tuples."""
    deck = []
    for rank in CARD_RANKS:
        value = CARD_VALUES[rank]
        # We only need the (rank, value) for scoring, suits are for representation
        for suit in SUITS:
            deck.append({'rank': rank, 'value': value, 'suit': suit})
    return deck

def calculate_hand_sum(hand):
    """Calculates the total sum of card values in a hand."""
    return sum(card['value'] for card in hand)

def format_card(card):
    """Formats a card for display."""
    return f"{card['rank']} of {card['suit']}"

def display_hand(player_name, hand, hand_sum):
    """Displays the hand and its sum."""
    cards_str = ', '.join([format_card(c) for c in hand])
    print(f"\n{player_name}'s Hand: {cards_str}")
    print(f"{player_name}'s Sum Total: {hand_sum}")

def play_game():
    print("--- Simple Three-Card Sum Poker ---")
    deck = create_deck()
    random.shuffle(deck)

    # Deal hands (3 cards each)
    player_hand = [deck.pop() for _ in range(3)]
    opponent_hand = [deck.pop() for _ in range(3)]

    # Calculate sums
    player_sum = calculate_hand_sum(player_hand)
    opponent_sum = calculate_hand_sum(opponent_hand)

    # Display results
    display_hand("Player", player_hand, player_sum)
    display_hand("Opponent", opponent_hand, opponent_sum)

    # Determine winner
    print("\n--- Result ---")
    if player_sum > opponent_sum:
        print(f"Player Wins! ({player_sum} > {opponent_sum})")
    elif opponent_sum > player_sum:
        print(f"Opponent Wins! ({opponent_sum} > {player_sum})")
    else:
        print(f"It's a Tie! Both sums are {player_sum}.")

if __name__ == "__main__":
    play_game()
