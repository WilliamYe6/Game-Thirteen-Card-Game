HEARTS, DIAMONDS, CLUBS, SPADES = 0, 1, 2, 3

TWO, THREE, FOUR, FIVE, SIX, SEVEN = 0, 1, 2, 3, 4, 5
EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE = 6, 7, 8, 9, 10, 11, 12

SUITS = [HEARTS, DIAMONDS, CLUBS, SPADES]
RANKS = [TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE]

SUITS_STR = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS_STR = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace']

def get_suit(card):
    return (card - 1) % 4

def get_rank(card):
    return (card - 1) // 4

def same_rank(card1, card2):
    return get_rank(card1) == get_rank(card2)

def same_suit(card1, card2):
    return get_suit(card1) == get_suit(card2)

def same_color_suit(card1, card2):
    suit1 = get_suit(card1)
    suit2 = get_suit(card2)
    both_red = (suit1 == HEARTS or suit1 == DIAMONDS) and (suit2 == HEARTS or suit2 == DIAMONDS)
    both_black = (suit1 == CLUBS or suit1 == SPADES) and (suit2 == SPADES or suit2 == CLUBS) 
    return both_red or both_black

def get_card(suit, rank):
    return (RANKS.index(rank) * 4) + SUITS.index(suit) + 1

CARDS_OF_RANK = [[get_card(suit, rank) for suit in SUITS] for rank in RANKS]
CARDS_OF_SUIT = [[get_card(suit, rank) for rank in RANKS] for suit in SUITS]

def card_to_string(card):
    return "{} of {}".format(RANKS_STR[get_rank(card)].upper(), SUITS_STR[get_suit(card)].upper())

hand_strs = dict()
def hand_to_string(hand):
    hand_t = tuple(hand)
    if hand_t not in hand_strs:
        s = ""
        for card in hand:
            s += card_to_string(card) + ", "
        hand_strs[hand_t] = s[:-2]
    return hand_strs[hand_t]

def get_deck():
    deck = []
    for suit in SUITS:
        for rank in RANKS:
            deck.append(get_card(suit, rank))
    return deck

def all_same_suit(cards):
    i = 1
    while i < len(cards):
        if not same_suit(cards[i-1], cards[i]):
            return False
        i += 1
    return True

def all_same_rank(cards):
    rank = get_rank(cards[0])
    return all(card in CARDS_OF_RANK[rank] for card in cards)
