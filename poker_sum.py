import random

def create_deck():
    """Creates a standard 52-card deck represented by numerical values.
    A=11, 2-10=face value, J/Q/K=10.
    """
    deck = []
    # Ranks 2 through 10 (4 of each)
    for value in range(2, 11):
        deck.extend([value] * 4)
    # Ranks J, Q, K (Value 10, 4 of each = 12 total)
    deck.extend([10] * 12)
    # Rank A (Value 11, 4 total)
    deck.extend([11] * 4)
    
    # Shuffling is not strictly necessary if we use random.sample later, but good practice.
    random.shuffle(deck)
    return deck

def draw_hand(deck, num_cards=3):
    """Draws a hand of cards from the deck without replacement.
    Returns the drawn hand and the remaining deck.
    """
    if len(deck) < num_cards:
        raise ValueError("Not enough cards in the deck.")

    # Draw cards randomly
    hand = random.sample(deck, num_cards)
    
    # Create a new list for the remaining deck by removing the drawn cards
    temp_deck = list(deck)
    for card in hand:
        # Remove the first occurrence of the card value found
        temp_deck.remove(card)
    
    return hand, temp_deck

def calculate_score(hand):
    """Calculates the sum of the card values in the hand."""
    return sum(hand)

def display_hand(hand):
    """Utility function to display card values and map A/10/J/Q/K for better readability."""
    mapping = {11: 'A', 10: '10/J/Q/K'}
    display = [mapping.get(c, str(c)) for c in hand]
    return f"[{', '.join(display)}] (Values: {hand})"

def play_game():
    print("--- Three Card Sum Poker Game ---")
    deck = create_deck()
    
    # 1. Draw Player Hand
    try:
        player_hand, deck = draw_hand(deck, 3)
        player_score = calculate_score(player_hand)
        
        print("\nPlayer draws 3 cards...")
        print(f"Player Hand: {display_hand(player_hand)}")
        print(f"Player Score (Sum): {player_score}")
        
        # 2. Draw Computer Hand
        computer_hand, deck = draw_hand(deck, 3)
        computer_score = calculate_score(computer_hand)

        print("\nComputer draws 3 cards...")
        print(f"Computer Hand: {display_hand(computer_hand)}")
        print(f"Computer Score (Sum): {computer_score}")

    except ValueError as e:
        print(f"Error drawing cards: {e}")
        return

    # 3. Compare Scores (Highest sum wins)
    print("\n--- Results ---")
    if player_score > computer_score:
        print(f"Player Wins! ({player_score} > {computer_score})")
    elif computer_score > player_score:
        print(f"Computer Wins! ({computer_score} > {player_score})")
    else:
        print("It's a Tie!")

if __name__ == "__main__":
    play_game()
