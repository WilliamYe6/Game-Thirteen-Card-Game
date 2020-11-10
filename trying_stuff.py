from arrangement import *
from card import *

def fct(a_hand,wildcard_rank):

    wanted_cards = []
    #if there is already a seq, cards +-1 max and min -> seq
    for elements in get_arrangement(a_hand, wildcard_rank):
        
        if is_valid_sequence(elements, wildcard_rank):
            
            if get_rank(max(elements)) < 13:
                wanted_cards += [get_card(get_suit(max(elements)), get_rank(max(elements)) + 1)]
            
            if get_rank(min(elements)) > 0:
                wanted_cards += [get_card(get_suit(min(elements)), get_rank(min(elements)) - 1)]

    return wanted_cards

fct([2, 3, 4, 8, 12], 10)
