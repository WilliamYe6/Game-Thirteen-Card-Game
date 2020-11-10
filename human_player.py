from card import *

def draw(hand, top_discard, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round):
    print("Hand:", hand_to_string(hand))
    loc = ''
    while loc != 'stock' and loc != 'discard':
        loc = input("Draw location (stock or discard): ")
    return loc

def discard(hand, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round):
    print("Hand:", hand_to_string(hand))
    for i, card in enumerate(hand):
        print(i, "\t", card_to_string(card))
    
    ind = -1
    while ind < 0 or ind >= len(hand):
        ind = input("Enter the index of the card to discard: ")
        if not ind.isdecimal():
            continue
        ind = int(ind)
    return hand[ind]
