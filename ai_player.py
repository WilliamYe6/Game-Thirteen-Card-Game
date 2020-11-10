#Authors: Aashiha Babu, Julia Kulenty, David Paquette, Christine Yang-Dai, William Ye
#Student ID (respectively):
from card import *
from arrangement import *
import doctest


def potential_arrangement(a_hand, wildcard_rank):
    '''(list, int) -> list

    Given a hand, returns a list of the cards that could potentially complete an arrangement.
    
    potential_arrangement([1, 5, 9, 13], 10) #wildcard not involved, 1 seq 
    [1, 5, 9, 13, 17]

    >>> potential_arrangement([1, 5, 9, 13], 3) #wildcard involved, 1 seq
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

    >>> potential_arrangement([25, 26, 27], 10) #wildcard not involved, 1 group
    [25, 26, 27, 28]

    >>> potential_arrangement([25, 26, 27], 6) #wildcard involved, 1 group
    [21, 22, 23, 25, 26, 27, 28, 29, 30, 31]

    >>> potential_arrangement([1, 2, 9, 13], 10) #wildcard not involved, 1 potential group (1 & 2 same rank)
    [1, 2, 3, 4, 5, 17]

    >>> potential_arrangement([32, 32, 48, 13], 11) #wildcard involved, 1 potential group (32 & 32 same rank)
    [9, 13, 14, 15, 16, 17, 28, 29, 30, 31, 32, 36, 44, 45, 46, 47, 48, 52]

    >>> potential_arrangement([2, 3, 4, 8, 12], 10) #wildcard not involved, 1 group (2, 3, 4) and 1 seq (4, 8, 12)
    [1, 2, 3, 4, 8, 12, 16]

    >>> potential_arrangement([2, 3, 4, 8, 12], 1) #wildcard involved, 1 group (2, 3, 4) and 1 seq (4, 8, 12)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16]

    >>> potential_arrangement([16, 24, 33, 47], 0) #wildcard not involved, 1 potential seq (16 & 24)
    [20]

    >>> potential_arrangement([16, 24, 33, 47], 11) #wildcard involved, 1 potential seq (16 & 24)
    [12, 13, 14, 15, 16, 20, 21, 22, 23, 24, 28, 29, 33, 34, 35, 36, 37, 45, 46, 47, 48, 51]

    >>> potential_arrangement([16, 24, 33, 12], 8) #wildcard involved, multiple potential seq (16, 24, 12)
    [8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24, 28, 29, 33, 34, 35, 36, 37]
    
    '''
    
    #list of the cards that could make the other players obtain an arrangement
    wanted_cards = []
    
    #compare cards in a_hand to see which cards are missing to complete an arrangement
    for j in range(len(a_hand)):
        
        #if there is a wildcard in a_hand
        if get_rank(a_hand[j]) == wildcard_rank:
            
            for i in range(len(a_hand)):
                
                #any same_suit with rank +- 1 gives an sequence
                if get_rank(a_hand[i]) < 13:
                    wanted_cards += [get_card(get_suit(a_hand[i]), (get_rank(a_hand[i])) + 1)]
                if get_rank(a_hand[i]) > 0:
                    wanted_cards += [get_card(get_suit(a_hand[i]), (get_rank(a_hand[i])) - 1)]
                    
                #any same_rank gives a group
                for n in range(0,4):
                    wanted_cards += [get_card(n, get_rank(a_hand[i]))]
                i += 1
                
        for i in range(len(a_hand)):
            
            #if 2 or more cards in a_hand have the same rank
            if same_rank(a_hand[j], a_hand[i]) and i != j:
                
                #any card with this rank gives a group
                for n in range(0,4):
                    wanted_cards += [get_card(n, get_rank(a_hand[i]))]
            
            #if card1 +-1 card2, then cards +-1 card1 and card2 -> seq       
            if abs(a_hand[j] - a_hand[i]) == 4:
                
                max_card = max([get_rank(a_hand[j]),get_rank(a_hand[i])])
                min_card = min([get_rank(a_hand[j]),get_rank(a_hand[i])])
                
                if get_rank(a_hand[i]) < 13 and get_rank(a_hand[j]) < 13:
                    wanted_cards += [get_card(get_suit(a_hand[i]), (max_card) + 1)]
                    
                if get_rank(a_hand[i]) > 0 and get_rank(a_hand[j]) > 0:
                    wanted_cards += [get_card(get_suit(a_hand[i]), (min_card) - 1)]
            
            #if card1 +-2 card2, then cards between card1 and 2 -> seq       
            if abs(a_hand[j] - a_hand[i]) == 8:
                
                max_card = max([get_rank(a_hand[j]),get_rank(a_hand[i])])
                min_card = min([get_rank(a_hand[j]),get_rank(a_hand[i])])
                
                wanted_cards += [get_card(get_suit(a_hand[i]), max_card - 1)]
            
            i += 1
        j += 1
    
    output_list = []
    
    #put the elements in order
    for e in range(len(wanted_cards)):
        output_list.append(min(wanted_cards))
        wanted_cards.remove(min(wanted_cards))
        
    #remove duplicate elements    
    for e in output_list:
        while output_list.count(e)>1:
            output_list.remove(e)
    
    return output_list

def draw(hand, top_discard, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round):
    '''(list, int, bool, list, int, int, int) -> str

    This function decides from where to pick up a card: from the discard pile or
    from the stock. It must return either the string stock or discard. Note that it can only draw from the
    discard pile if the top_discard card is not None. 
    '''
    
    if top_discard == wildcard_rank:
        return 'discard'

def discard(hand, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round):
    '''(list, bool, list, int, int, int) -> int
    This function decides which card to discard from the hand list and returns it.

    >>> hand = [10, 49, 50, 51, 52]
    >>> last_turn = False
    >>> picked_up_discard_cards = [[16, 24, 33, 47], [2, 3, 4, 8, 12], [1, 5, 9, 13]]
    >>> player_position = 2
    >>> wildcard_rank = 9
    >>> num_turns_this_round = 0
    >>> x = discard(hand, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round)
    >>> x
    10
    
    '''
    #a list of cards that can be discarded
    discard_cards = []
    for card in hand:
        #cards in our hand that are not part of a sequence nor a group
        if card not in get_arrangement(hand, wildcard_rank):
            discard_cards += [card]
    
    #list containing "penalty" points associated to the cards that can be discarded
    discard_value = [] 
    for i in range(len(discard_cards)):
        
        turn_multiplier = 1
        
        if last_turn:
            turn_multiplier = 3
        
        points = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1]
        discard_value += [points[RANKS.index(get_rank(discard_cards[i]))]] * turn_multiplier

        #if player_position != : #to do, if the player is the last player to play before the round ends,
        #then don't care about the following:
        for others_hand in picked_up_discard_cards:
            if discard_cards[i] in potential_arrangement(others_hand, wildcard_rank):
                discard_value[i] = discard_value[i] / 2 #TBD
    
        #to discard the card with the highest penalty point
    
    return discard_cards[discard_value.index(max(discard_value))] #the card with the highest value will be discarded