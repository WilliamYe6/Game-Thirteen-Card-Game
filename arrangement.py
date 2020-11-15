import math
import doctest
from card import *
from collections import Counter
from itertools import chain, combinations

def equal_occurrences(l1, l2):
    for x in l1:
        num = 0
        for y in l1:
            if x == y:
                num += 1
        num2 = 0
        for y in l2:
            if x == y:
                num2 += 1
        if num != num2:
            return False
    return True

def is_valid_arrangement(arrangement, hand, wildcard_rank):
    """ (tuple<Group/Sequence>, list<Card>, RANK) -> bool
    
    >>> hand = [get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE), get_card(SPADES, FIVE)]
    >>> wildcard_rank = FIVE
    >>> arrangement = get_arrangement(hand, wildcard_rank)
    >>> is_valid_arrangement(arrangement, hand, wildcard_rank)
    False
    """
    cards = []
    for seq in arrangement:
        if not is_valid_group(seq, wildcard_rank) and not is_valid_sequence(seq, wildcard_rank):
            return False
        
        cards.extend(seq)
    
    return equal_occurrences(hand, cards)

def remove_wildcards_from_hand(hand, wildcard_rank, num_cards):
    """ (list<Card>, RANK) -> int
    Removes all wildcards from the hand and returns the number of wildcards removed.
    
    >>> hand = [get_card(SPADES, TWO), get_card(SPADES, THREE), get_card(SPADES, FOUR)]
    >>> remove_wildcards_from_hand(hand, THREE, len(hand))
    1
    >>> hand
    [4, 12]
    """
    hand[:] = [card for card in hand if card not in CARDS_OF_RANK[wildcard_rank]]
    return num_cards - len(hand)

valid_groups = dict()
def is_valid_group(cards, wildcard_rank):
    """ (tuple<Card>, int) -> bool
    Checks if the given list of cards forms a valid group.
    A group is a set of three or more cards of the same rank.
    A wildcard (card of the given wildcard rank) can fit in any group.
    >>> is_valid_group([get_card(HEARTS, TWO), get_card(HEARTS, TWO), get_card(CLUBS, TWO)], KING)
    True
    >>> is_valid_group([get_card(HEARTS, FOUR), get_card(HEARTS, TWO), get_card(CLUBS, TWO)], KING)
    False
    >>> is_valid_group([get_card(HEARTS, TWO), get_card(CLUBS, TWO)], KING)
    False
    >>> is_valid_group([get_card(HEARTS, TWO), get_card(CLUBS, TWO), get_card(SPADES, KING)], KING)
    True
    >>> is_valid_group([get_card(CLUBS, THREE), get_card(HEARTS, FOUR), get_card(SPADES, FOUR)], THREE)
    True
    >>> is_valid_group([get_card(CLUBS, THREE), get_card(HEARTS, FOUR), get_card(SPADES, FOUR)], FOUR)
    True
    >>> is_valid_group([get_card(CLUBS, THREE), get_card(HEARTS, THREE), get_card(SPADES, THREE), get_card(DIAMONDS, THREE)], FOUR)
    True
    >>> is_valid_group([get_card(CLUBS, THREE), get_card(HEARTS, THREE), get_card(SPADES, THREE), get_card(DIAMONDS, THREE), get_card(CLUBS, FOUR)], FOUR)
    True
    >>> is_valid_group([get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE), get_card(SPADES, FIVE)], FIVE)
    False
    """
    if type(cards) is not tuple:
        cards = tuple(cards)

    num_cards = len(cards)
    if num_cards < 3:
        return False

    if (cards, wildcard_rank) not in valid_groups:
        cards_list = list(cards)
        result = True
        
        num_wildcards = remove_wildcards_from_hand(cards_list, wildcard_rank, num_cards)
        if num_cards == num_wildcards:
            result = True
        else:
            #assert len(cards_list) >= 3-num_wildcards
            cards_list.sort()
        
            group_rank = get_rank(cards_list[0])
            for card in cards_list[1:]:
                card_rank = get_rank(card)
                #assert card_rank != wildcard_rank
                if card_rank != group_rank:
                    result = False
                    break
        valid_groups[(cards, wildcard_rank)] = result
    
    return valid_groups[(cards, wildcard_rank)]

valid_sequences = dict()
def is_valid_sequence(cards, wildcard_rank):
    """ (tuple<Card>, int) -> bool
    Checks if the given list of cards forms a valid sequence.
    A sequence is a set of three or more cards of the same suit with consecutive rank.
    A wildcard (card of the given wildcard rank) can fit in any sequence.
    >>> is_valid_sequence([], KING)
    False
    >>> is_valid_sequence([get_card(HEARTS, TWO), get_card(HEARTS, THREE), get_card(HEARTS, FOUR)], KING)
    True
    >>> is_valid_sequence([get_card(HEARTS, TWO), get_card(HEARTS, THREE), get_card(HEARTS, TEN)], KING)
    False
    >>> is_valid_sequence([get_card(HEARTS, TWO), get_card(HEARTS, FOUR), get_card(HEARTS, TEN)], TEN)
    True
    >>> is_valid_sequence([get_card(HEARTS, TWO), get_card(HEARTS, FIVE), get_card(HEARTS, TEN)], TEN)
    False
    >>> is_valid_sequence([get_card(HEARTS, TWO), get_card(HEARTS, THREE), get_card(HEARTS, TEN)], TEN)
    True
    >>> is_valid_sequence([get_card(SPADES, THREE), get_card(SPADES, JACK), get_card(SPADES, KING)], THREE)
    True
    >>> is_valid_sequence([get_card(CLUBS, NINE), get_card(CLUBS, JACK), get_card(CLUBS, JACK)], THREE)
    False
    >>> is_valid_sequence([get_card(CLUBS, NINE), get_card(CLUBS, JACK), get_card(CLUBS, JACK)], JACK)
    True
    >>> is_valid_sequence([get_card(CLUBS, NINE), get_card(CLUBS, JACK), get_card(CLUBS, JACK), get_card(CLUBS, KING)], JACK)
    False
    >>> is_valid_sequence([get_card(CLUBS, NINE), get_card(CLUBS, JACK), get_card(CLUBS, JACK), get_card(CLUBS, QUEEN)], JACK)
    True
    >>> is_valid_sequence([get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE)], FIVE)
    False
    >>> is_valid_sequence([get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE)], FIVE)
    False
    >>> is_valid_sequence([get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE), get_card(SPADES, FIVE)], FIVE)
    False
    """
    if type(cards) is not tuple:
        cards = tuple(cards)
    
    num_cards = len(cards)
    if num_cards < 3:
        return False
    
    if (cards, wildcard_rank) not in valid_sequences:
        cards_list = list(cards)
        result = True
        cards_list.sort()
        
        num_wildcards = remove_wildcards_from_hand(cards_list, wildcard_rank, num_cards)
        #assert len(cards_list) >= 3-num_wildcards
        
        if num_cards == num_wildcards:
            result = True
        elif not all_same_suit(cards_list):
            result = False
        else:
            # determine amount of gap in sequence, if any
            i = 1
            gaps = 0
            num_cards = len(cards_list)
            while i < num_cards:
                if get_rank(cards_list[i]) == get_rank(cards_list[i-1]):
                    # can't have two cards of same rank in a sequence if they are not wildcards
                    result = False
                    break
                if get_rank(cards_list[i]) != get_rank(cards_list[i-1])+1:
                    gaps += (get_rank(cards_list[i]) - get_rank(cards_list[i-1])) - 1
                i += 1
            
            if result:
                result = gaps <= num_wildcards # check if we can fill the gaps with wildcards
        
        valid_sequences[(cards, wildcard_rank)] = result
    
    return valid_sequences[(cards, wildcard_rank)]

def arrangement_to_string(arrangement):
    s = ''
    i = 1
    for seq in arrangement:
        s += str(i) + "\t" + hand_to_string(seq) + "\n"
        i += 1
    return s

occurrences = {}
element_counts = {}
nested_tuple_counts = {}
def equal_or_less_occurrences(elements, nested_tuple):
    if (elements, nested_tuple) not in occurrences:
        result = True
        
        if elements not in element_counts:
            e_cts = Counter(elements)
            element_counts[elements] = e_cts
        else:
            e_cts = element_counts[elements]
        if nested_tuple not in nested_tuple_counts:
            nt_cts = Counter(chain.from_iterable(nested_tuple))
            nested_tuple_counts[nested_tuple] = nt_cts
        else:
            nt_cts = nested_tuple_counts[nested_tuple]
                
        if any(nt_cts[x] > e_cts[x] for x in elements):
            result = False
        
        occurrences[(elements, nested_tuple)] = result
    return occurrences[(elements, nested_tuple)]

count_elements_cache = {}
def count_elements(nested_tuple):
    if nested_tuple not in count_elements_cache:
        count_elements_cache[nested_tuple] = sum(len(x) for x in nested_tuple)
    return count_elements_cache[nested_tuple]

def more_than(nested_tuple, num):
    ct = 0
    for tup in nested_tuple:
        ct += len(tup)
        if ct >= num:
            return True
    return False

best_arrangements = {}
def get_arrangement(hand, wildcard_rank):
    """ (list<Card>, RANK) -> tuple<tuple<Card>>
    
    The two 3's and two wildcards will be put into a group of four Three's.
    >>> hand = [get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE), get_card(SPADES, FIVE)]
    >>> wildcard_rank = FIVE
    >>> solution = ((get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE), get_card(SPADES, FIVE)),)
    >>> get_arrangement(hand, wildcard_rank) == solution
    True
    """
    len_hand = len(hand)
    if len_hand < 3:
        return []
    
    hand = hand[:]
    hand.sort()
    hand_t = tuple(hand)
    
    if (hand_t, wildcard_rank) in best_arrangements:
        return best_arrangements[(hand_t, wildcard_rank)]
    
    valid_combinations = set()
    stop = False
    for group_length in range(len_hand, 2, -1):
        for combination in combinations(hand, group_length):
            if is_valid_group(combination, wildcard_rank) or is_valid_sequence(combination, wildcard_rank):
                valid_combinations.add(combination)
                if group_length == len_hand: # don't keep looking if we found a combo for entire hand
                    stop = True
                    break
        if stop:
            break
    
    if len(valid_combinations) <= 1:
        if len(valid_combinations) == 0:
            best_arrangements[(hand_t, wildcard_rank)] = []
        elif len(valid_combinations) == 1:
            best_arrangements[(hand_t, wildcard_rank)] = list(valid_combinations)
        return best_arrangements[(hand_t, wildcard_rank)]
    
    # find optimal combination of groups and sequences
    cur_max_arrangements = []
    cur_max_arranged_cards = 0
    max_possible_arrangements = min(len(valid_combinations), len_hand // 3)
    for num_sequences in range(max_possible_arrangements, -1, -1):
        for arrangement in combinations(valid_combinations, num_sequences):
            if arrangement in cur_max_arrangements:
                continue
            #num_cards_in_sequence = count_elements(arrangement)
            if more_than(arrangement, cur_max_arranged_cards) and equal_or_less_occurrences(hand_t, arrangement):
                num_cards_in_sequence = count_elements(arrangement)
                if num_cards_in_sequence > cur_max_arranged_cards:
                    cur_max_arranged_cards = num_cards_in_sequence
                    cur_max_arrangements = [arrangement]
                elif num_cards_in_sequence == cur_max_arranged_cards:
                    cur_max_arrangements.append(arrangement)
    
    if cur_max_arranged_cards == len_hand:
        best_arrangement = cur_max_arrangements[0]
    else:
        best_arrangement = get_min_penalty_arrangement(tuple(cur_max_arrangements), hand_t)
    
    #assert best_arrangement is not None       
    best_arrangements[(hand_t, wildcard_rank)] = best_arrangement
    return best_arrangement

min_penalty_cache = {}
def get_min_penalty_arrangement(cur_max_arrangements, hand):
    if (cur_max_arrangements, hand) not in min_penalty_cache:
        min_point_val = math.inf
        best_arrangement = None
        points = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1]
        for arrangement in cur_max_arrangements:
            unarranged_cards = list(hand)
            for seq in arrangement:
                for card in seq:
                    unarranged_cards.remove(card)
            point_value = 0
            for card in unarranged_cards:
                point_value += points[RANKS.index(get_rank(card))]
            if point_value < min_point_val:
                min_point_val = point_value
                best_arrangement = arrangement
        min_penalty_cache[(cur_max_arrangements, hand)] = best_arrangement
    return min_penalty_cache[(cur_max_arrangements, hand)]

def clear_caches():
    occurrences.clear()
    element_counts.clear()
    nested_tuple_counts.clear()
    best_arrangements.clear()
    count_elements_cache.clear()
    min_penalty_cache.clear()

if __name__ == "__main__": 
    doctest.testmod()