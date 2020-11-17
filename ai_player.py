#Authors: Aashiha Babu, Julia Kulenty, David Paquette, Christine Yang-Dai, William Ye
#Student ID (respectively):
from card import *
from arrangement import *
import doctest

def complete_arrangement(a_hand, wildcard_rank):
    '''(list, int) -> list
    Given a hand, returns a list of the cards that could potentially complete an arrangement if added to hand.
    
    >>> complete_arrangement([1, 5, 9, 13], 10) #wildcard not involved, 1 seq 
    [1, 5, 9, 13, 17]

    >>> complete_arrangement([1, 5, 9, 13], 3) #wildcard involved, 1 seq
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

    >>> complete_arrangement([25, 26, 27], 10) #wildcard not involved, 1 group
    [25, 26, 27, 28]

    >>> complete_arrangement([25, 26, 27], 6) #wildcard involved, 1 group
    [21, 22, 23, 25, 26, 27, 28, 29, 30, 31]

    >>> complete_arrangement([1, 2, 9, 13], 10) #wildcard not involved, 1 potential group (1 & 2 same rank)
    [1, 2, 3, 4, 5, 17]

    >>> complete_arrangement([32, 32, 48, 13], 11) #wildcard involved, 1 potential group (32 & 32 same rank)
    [9, 13, 14, 15, 16, 17, 28, 29, 30, 31, 32, 36, 44, 45, 46, 47, 48, 52]

    >>> complete_arrangement([2, 3, 4, 8, 12], 10) #wildcard not involved, 1 group (2, 3, 4) and 1 seq (4, 8, 12)
    [1, 2, 3, 4, 8, 12, 16]

    >>> complete_arrangement([2, 3, 4, 8, 12], 1) #wildcard involved, 1 group (2, 3, 4) and 1 seq (4, 8, 12)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16]

    >>> complete_arrangement([16, 24, 33, 47], 0) #wildcard not involved, 1 potential seq (16 & 24)
    [20]

    >>> complete_arrangement([16, 24, 33, 47], 11) #wildcard involved, 1 potential seq (16 & 24)
    [12, 13, 14, 15, 16, 20, 21, 22, 23, 24, 28, 29, 33, 34, 35, 36, 37, 43, 45, 46, 47, 48, 51]***************************************

    >>> complete_arrangement([16, 24, 33, 12], 8) #wildcard involved, multiple potential seq (16, 24, 12)
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
                if get_rank(a_hand[i]) < 12:
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
            
            #if the rank of card1 +- 1 = rank of card2, then cards sequence is formed when 
            #a card from the same suit with a rank higher than card2 or lower than card 1 is drawn
            if abs(a_hand[j] - a_hand[i]) == 4:
                
                max_card = max([get_rank(a_hand[j]),get_rank(a_hand[i])])
                min_card = min([get_rank(a_hand[j]),get_rank(a_hand[i])])
                
                if max_card < 12:
                    wanted_cards += [get_card(get_suit(a_hand[i]), (max_card) + 1)]
                    
                if min_card > 0:
                    wanted_cards += [get_card(get_suit(a_hand[i]), (min_card) - 1)]
            
            #if the rank of card1 +- 2 = rank of card2, then cards sequence is formed when
            #a card from the same suit with a rank higher between card2 and card1 is drawn      
            if abs(a_hand[j] - a_hand[i]) == 8:
                max_card = max([get_rank(a_hand[j]),get_rank(a_hand[i])])
                wanted_cards += [get_card(get_suit(a_hand[i]), max_card - 1)]
            
            i += 1
        j += 1
    
    #put the elements in order
    wanted_cards.sort()
    
    #remove duplicate elements    
    for e in wanted_cards:
        while wanted_cards.count(e)>1:
            wanted_cards.remove(e)
    
    return wanted_cards

def second_best_draw(hand, wildcard_rank):
    """(list,int)-->list

    If there is no arrangement to be made, given the hand, the card
    at the top of the discard pile, and the wildcard rank, the function
    will return of the next most useful cards for the function to pick up.
    
    >>> second_best_draw([1, 7, 22], 3)
    [2, 3, 4, 5, 6, 8, 9, 11, 13, 14, 15, 16, 18, 21, 23, 24, 26, 30]
    
    >>> second_best_draw([9, 22, 43, 28], 4)
    [1, 5, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 30, 32, 35, 36, 39, 41, 42, 44, 47, 51]
    
    >>> second_best_draw([12, 33, 24, 40, 39], 5)
    [4, 8, 9, 10, 11, 12, 16, 17, 20, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 34, 35, 36, 37, 38, 39, 40, 40, 41, 43, 44, 45, 47, 48, 49, 51, 52]
    
    """
    #cards that could be useful for the person to pick up
    useful_cards = []
    
    #The deck of total cards
    deck = get_deck()
    
    #all cards that are wildcard ranks for the turn 
    for i in range(len(deck)):
        if (get_rank(deck[i]) == wildcard_rank) and (deck[i] not in hand):
            useful_cards.append(deck[i])
           
    #cards of same rank but different suit (group)
    for i in range(len(deck)):
        x = get_rank(deck[i])
        
        for j in range(len(hand)):
            y=get_rank(hand[j])
            
            if (x==y) and (deck[i] != hand[j]):
                useful_cards.append(deck[i])
            
    #same suit but one or two difference in rank (sequence)
    for i in range(len(deck)):
        for j in range(len(hand)):
            
            if same_suit(deck[i],hand[j]):
                x = get_rank(deck[i])
                y = get_rank(hand[j])
                diff_in_ranks = abs(x - y)
                
                if (diff_in_ranks <= int(2/3 * (wildcard_rank + 2 ))) and (deck[i] != hand[j]):
                    useful_cards.append(deck[i])
          
    #Getting rid of duplicates and ordering  
    for i in useful_cards:
        if useful_cards.count(i)>1:
            useful_cards.remove(i)
            
    #sorting the cards
    useful_cards.sort()
    
    return useful_cards

def single_card_points(card):
    ''' (int) -> int
    Returns the points a single card is worth.
    >>> single_card_points(21)
    7
    >>> single_card_points(52)
    1
    >>> single_card_points(45)
    10
    '''
    if get_rank(card) in RANKS[:8]:
        return get_rank(card) + 2
    elif get_rank(card) in RANKS[8:12]:
        return 10
    elif get_rank(card) in RANKS[12:]:
        return 1

def draw(hand, top_discard, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round):
    '''(list, int, bool, list, int, int, int) -> str

    This function picks a card from the discard pile and returns 'discard'
    or picks a card from the stock pile and returns 'stock'.
    It will automatically draw from the stock pile if the top_discard card is None.
    
    >>> draw([1, 2, 3, 47, 48], None, False, [3, 6, 19, 4], 2, 5, 4)
    'stock'
    >>> draw([1, 2, 3, 47, 48], 22, False, [3, 6, 19, 4], 2, 5, 4)
    'discard'
    >>> draw([1, 2, 3, 47, 48], 38, False, [3, 6, 19, 4], 2, 5, 4)
    'stock'
    >>> draw([1, 2, 3, 38, 51], 4, False, [3, 6, 19, 4], 2, 5, 4)
    'discard'
    >>> draw([1, 2, 3, 4, 48], 24, True, [3, 6, 19, 4], 2, 5, 4)
    'discard'
    >>> draw([1, 2, 3, 4, 24], 48, True, [3, 6, 19, 4], 2, 5, 4)
    'stock'
    >>> draw([37, 10, 35], 21, False, [], 0, 3, 0)
    '''
    
    print('Hand:', hand_to_string(hand))
    
    get_arrangement_list = []
    for tuples in get_arrangement(tuple(hand), wildcard_rank):
        get_arrangement_list += list(tuples)
    
    #No cards in the discard pile
    if top_discard == None:
        return 'stock'
    
    #When it is last turn
    if last_turn:
        #If the top_discard card can form an arrangement or its penalty points are low, take it
        if top_discard in complete_arrangement(hand, wildcard_rank) or single_card_points(top_discard) < 8:
            return 'discard'
        #else, there is a 50% chances of picking a low penalty point card in the stock pile in a complete deck
        else:
            return 'stock'
    #when it is not the last turn    
    else:
        
        #counting the number of cards left to discard
        discard_cards = []
        for card in hand:
            if card not in get_arrangement_list:
                discard_cards += [card]
        
        #if there is only one card left to discard, do not pick from discard
        if len(discard_cards) == 1 and top_discard not in complete_arrangement(hand, wildcard_rank):
            return 'stock'
        #Not last turn and top card of discard pile is of the same rank as the wildcard OR
        #Not last turn and top card of discard pile forms an arrangement OR
        #Not last turn and top card of discard pile will form an arrangement then pick from discard pile
        elif ((get_rank(top_discard) == wildcard_rank or top_discard in complete_arrangement(hand, wildcard_rank)) or (top_discard in second_best_draw(hand, wildcard_rank))):
            return 'discard'
        else:
            return 'stock'

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
    
    >>> hand = [45, 46, 47, 8]
    >>> last_turn = False
    >>> picked_up_discard_cards = []
    >>> player_position = 4
    >>> wildcard_rank = 5
    >>> num_turns_this_round = 7
    >>> x = discard(hand, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round)
    >>> x

    ONE MORE EXAMPLEEE
    '''
    #a list of cards that can be discarded
    discard_cards = []
    
    #making a list from the get arrangement tuple of tuple
    get_arrangement_list = []
    for tuples in get_arrangement(tuple(hand), wildcard_rank):
        get_arrangement_list += list(tuples)
    
    for card in hand:
        #when its the last turn, 
        if last_turn:
            #the cards in our hand that are not part of a sequence nor a group are useless
            if card not in get_arrangement_list:
                discard_cards += [card]
        else:
        #in a normal turn, cards in our hand that are not part of a sequence nor a group
        #and cards that cannot help us form a sequence or a group are useless
            if card not in get_arrangement_list and card not in second_best_draw(hand, wildcard_rank):
                discard_cards += [card]
    
    #if no card is useless, the priority is to form groups
    #because there is a higher chance of forming a group than a sequence
    if len(discard_cards) == 0:
        rank_of_hand = []
        for i in range(len(hand)):
            rank_of_hand += [get_rank(hand[i])]
            
        for i in range(len(hand)):
            if (get_rank(hand[i]) != wildcard_rank) and (get_rank(hand[i]) not in (rank_of_hand[:i] + rank_of_hand[(i + 1):])):
                discard_cards += [hand[i]]
                                    
    #if all the potential arrangement are groups, then any card could be discarded
    if len(discard_cards) == 0:
        for card in hand:
            if get_rank(card) != wildcard_rank:
                discard_cards += [card]
    
    #list containing "penalty" points associated to the cards that can be discarded
    discard_value = []
    
    #if it is the last turn, it is more important to discard higher value cards
    turn_multiplier = 1
    if last_turn:
        turn_multiplier = 3
    
    for i in range(len(discard_cards)):
        
        #the penalty point associated to each card in ours hand that is not a part of an arrangement
        points = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1]
        discard_value += [points[RANKS.index(get_rank(discard_cards[i]))]*turn_multiplier]
        
        #discarding cards in complete_arrangement gives an advantage to other players,
        for others_hand in picked_up_discard_cards:
                for cards in others_hand:
                    others_hand.count(cards) > 1
            #if discard_cards[i] in complete_arrangement(others_hand, wildcard_rank):
                    discard_value[i] = discard_value[i] / 2 #so the penalty value is disminished

    #the card with the highest value will be discarded
    return discard_cards[discard_value.index(max(discard_value))]
#doctest.testmod()

hand = [52, 51, 5, 7, 1]
last_turn = False
picked_up_discard_cards = [[]]
player_position = 0
wildcard_rank = 2
num_turns_this_round = 19
x = discard(hand, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round)