import random

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['Ace'] + [str(n) for n in range(2, 11)] + ['Jack', 'Queen']
RANK_VALUES = {rank: i+1 for i, rank in enumerate(RANKS)}  # Ace=1, ..., Queen=12

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = RANK_VALUES[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def deal(self, num):
        dealt = self.cards[:num]
        self.cards = self.cards[num:]
        return dealt

    def reveal_card(self):
        if self.cards:
            card = self.cards.pop(0)
            print(f"Revealed card: {card}")
        else:
            print("No cards left to reveal.")

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def show_hand(self):
        for i, card in enumerate(self.hand, 1):
            print(f"{i}: {card}")

    def play_card(self, lead_suit=None):
        self.show_hand()
        while True:
            try:
                choice = int(input(f"{self.name}, choose a card to play (1-{len(self.hand)}): "))
                chosen_card = self.hand[choice - 1]
                if lead_suit and any(card.suit == lead_suit for card in self.hand):
                    if chosen_card.suit != lead_suit:
                        print(f"You must follow suit: {lead_suit}")
                        continue
                return self.hand.pop(choice - 1)
            except (ValueError, IndexError):
                print("Invalid choice. Try again.")

def determine_round_winner(card1, card2, lead_suit):
    if card1.suit == lead_suit and card2.suit != lead_suit:
        return 1
    elif card2.suit == lead_suit and card1.suit != lead_suit:
        return 2
    elif card1.suit == lead_suit and card2.suit == lead_suit:
        return 1 if card1.value > card2.value else 2
    return 1  # Default fallback

def play_game():
    deck = Deck()
    p1 = Player("Player 1")
    p2 = Player("Player 2")

    p1.hand = deck.deal(8)
    p2.hand = deck.deal(8)

    leader = random.choice([p1, p2])
    print(f"{leader.name} will lead first.")

    rounds_played = 0
    while rounds_played < 16:
        print("\n--- New Round ---")
        print(f"{leader.name} leads.")

        lead_card = leader.play_card()
        follower = p1 if leader == p2 else p2
        follow_card = follower.play_card(lead_card.suit)

        print(f"{leader.name} played {lead_card}")
        print(f"{follower.name} played {follow_card}")

        winner_num = determine_round_winner(lead_card, follow_card, lead_card.suit)
        round_winner = leader if winner_num == 1 else follower
        round_winner.score += 1
        print(f"{round_winner.name} wins the round and now has {round_winner.score} point(s).")

        deck.reveal_card()
        rounds_played += 1

        # Check for 4-card hands, deal 4 more if needed
        if len(p1.hand) == 4 and len(p2.hand) == 4 and len(deck.cards) >= 8:
            print("\nBoth players draw 4 more cards.")
            p1.hand += deck.deal(4)
            p2.hand += deck.deal(4)

        # Early end condition
        if p1.score >= 9 and p2.score >= 1:
            print("Player 1 has clinched the win!")
            break
        elif p2.score >= 9 and p1.score >= 1:
            print("Player 2 has clinched the win!")
            break

        leader = round_winner

    print("\n--- Game Over ---")
    if p1.score == 0 and p2.score == 16:
        print("Player 1 shot the moon! Final score: 17-0. Player 1 wins!")
    elif p2.score == 0 and p1.score == 16:
        print("Player 2 shot the moon! Final score: 0-17. Player 2 wins!")
    elif p1.score > p2.score:
        print(f"Player 1 wins! {p1.score} to {p2.score}")
    elif p2.score > p1.score:
        print(f"Player 2 wins! {p2.score} to {p1.score}")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_game()
