#Authors: Aashiha Babu, Julia Kulenty, David Paquette, Christine Yang-Dai, William Ye
#Student ID (respectively):

def potential_arrangement(a_hand, wildcard_rank):
    '''(list, int) -> list

    Given a hand, returns a list of the cards that could potentially complete an arrangement.
    
    >>> potential_arrangement([1, 5, 9, 13], 10)
    []
    
    >>> potential_arrangement([1, 5, 9, 13], 3)
    [5, 1, 2, 3, 4, 9, 1, 5, 6, 7, 8, 13, 5, 9, 10, 11, 12, 17, 9, 13, 14, 15, 16]
    
    >>> potential_arrangement([1, 2, 9, 13], 10)
    [1, 2, 3, 4, 1, 2, 3, 4]
    
    >>> potential_arrangement([32, 32, 48, 13], 10)
    [29, 30, 31, 32, 29, 30, 31, 32]
    
    >>> potential_arrangement([2, 3, 4, 8, 12], 10)
    [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
    
    >>> potential_arrangement([2, 3, 4, 8, 12], 1)
    [6, 1, 2, 3, 4, 7, 1, 2, 3, 4, 8, 1, 2, 3, 4, 4, 12, 5, 6, 7, 8, 8, 16, 9, 10, 11, 12, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
    '''
    #list of the cards that could make the other players obtain an arrangement
    wanted_cards = []
    
    #compare cards in a_hand to see which cards are missing to complete an arrangement
    for j in range(len(a_hand)):
        #if there is a wildcard in a_hand
        if get_rank(a_hand[j]) == wildcard_rank:
            
            for i in range(len(a_hand)):
                #any same_suit with rank +- 1 gives an sequence
                if a_hand[i] + 1 <= 52:
                    wanted_cards += [get_card(get_suit(a_hand[i]), get_rank(a_hand[i]) + 1)]
                if a_hand[i] - 1 >= 1:
                    wanted_cards += [get_card(get_suit(a_hand[i]), get_rank(a_hand[i]) - 1)]
                #any same_rank gives a group
                wanted_cards += [get_card(0, get_rank(a_hand[i])), get_card(1, get_rank(a_hand[i])), get_card(2, get_rank(a_hand[i])), get_card(3, get_rank(a_hand[i]))]
                i += 1
                
        for i in range(len(a_hand)):
            #if 2 or more cards in a_hand have the same rank
            if same_rank(a_hand[j], a_hand[i]) and i != j:
                #any card with this rank gives a group
                wanted_cards += [get_card(0, get_rank(a_hand[j])), get_card(1, get_rank(a_hand[j])), get_card(2, get_rank(a_hand[j])), get_card(3, get_rank(a_hand[j]))]
            i += 1
        j += 1
        
    return wanted_cards
        #if card1 +-1 card2, then cards +-1 card1 and card2 -> seq
        #if card1 +-2 card2, then cards between card1 and 2 -> seq
        #if there is already a group, cards +-1 max and min -> seq

def draw(hand, top_discard, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round):
    '''(list, int, bool, list, int, int, int) -> str

    This function decides from where to pick up a card: from the discard pile or
    from the stock. It must return either the string stock or discard. Note that it can only draw from the
    discard pile if the top_discard card is not None. To aid in your decision, the function has the following
    parameters
    '''
    if top_discard == wildcard_rank:
        return 'discard'

def discard(hand, last_turn, picked_up_discard_cards, player_position, wildcard_rank, num_turns_this_round):
    
    #a list of cards that can be discarded
    discard_cards = []
    for card in hand:
        #cards in our hand that are not part of a sequence nor a group
        if card not in get_arrangement(arrangement, hand, wildcard_rank):
            discard_cards += card
    
    #list containing "penalty" points associated to the cards that can be discarded
    discard_value = [] 
    for card in discard_cards:
        points = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1]
        discard_value += [points[RANKS.index(get_rank(card))]]
                             
        if discard_cards[i] in potential_arrangement:
            discard_value -= 
    
        #cards in our hand that are not part of a sequence nor a group
        if not is_valid_arrangement(arrangement, hand, wildcard_rank):
            #if player_position != : #to do, if the player is the last player to play before the round ends,
            #then don't care about the following:
            for others_hand in picked_up_discard_cards:
                if #cards not in almost arrangement:
                    to_discard += cards
    
    #to discard the card with the highest penalty point
    if last_turn:
        return max(to_discard) #the card with the highest value will be discarded