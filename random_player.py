import random
from card import *

def draw(hand, top_discard, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round):
    if top_discard is not None:
        return random.choice(['stock', 'discard'])
    return 'stock'

def discard(hand, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round):
    return random.choice(hand)
