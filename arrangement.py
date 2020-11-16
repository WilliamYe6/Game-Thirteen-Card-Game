import math
import doctest
from card import *
from functools import lru_cache
from itertools import combinations

LRU_CACHE_SIZE = 500

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

@lru_cache(maxsize=LRU_CACHE_SIZE)
def is_valid_arrangement(arrangement, hand, wildcard_rank):
    """ (tuple<Group/Sequence>, tuple<Card>, RANK) -> bool
    
    >>> hand = tuple([get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE), get_card(SPADES, FIVE)])
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

@lru_cache(maxsize=2)
def remove_wildcards_from_hand(hand, wildcard_rank, num_cards):
    """ (tuple<Card>, RANK) -> (list<Card>, int)
    Returns the hand without wildcards and returns the number of wildcards removed.
    
    >>> hand = tuple([get_card(SPADES, TWO), get_card(SPADES, THREE), get_card(SPADES, FOUR)])
    >>> remove_wildcards_from_hand(hand, THREE, len(hand))
    (1, [4, 12])
    """
    hand = [card for card in hand if card not in CARDS_OF_RANK[wildcard_rank]]
    return (num_cards - len(hand), hand)

@lru_cache(maxsize=LRU_CACHE_SIZE)
def is_valid_group(cards, wildcard_rank):
    """ (tuple<Card>, int) -> bool
    Checks if the given list of cards forms a valid group.
    A group is a set of three or more cards of the same rank.
    A wildcard (card of the given wildcard rank) can fit in any group.
    >>> is_valid_group(tuple([get_card(HEARTS, TWO), get_card(HEARTS, TWO), get_card(CLUBS, TWO)]), KING)
    True
    >>> is_valid_group(tuple([get_card(HEARTS, FOUR), get_card(HEARTS, TWO), get_card(CLUBS, TWO)]), KING)
    False
    >>> is_valid_group(tuple([get_card(HEARTS, TWO), get_card(CLUBS, TWO)]), KING)
    False
    >>> is_valid_group(tuple([get_card(HEARTS, TWO), get_card(CLUBS, TWO), get_card(SPADES, KING)]), KING)
    True
    >>> is_valid_group(tuple([get_card(CLUBS, THREE), get_card(HEARTS, FOUR), get_card(SPADES, FOUR)]), THREE)
    True
    >>> is_valid_group(tuple([get_card(CLUBS, THREE), get_card(HEARTS, FOUR), get_card(SPADES, FOUR)]), FOUR)
    True
    >>> is_valid_group(tuple([get_card(CLUBS, THREE), get_card(HEARTS, THREE), get_card(SPADES, THREE), get_card(DIAMONDS, THREE)]), FOUR)
    True
    >>> is_valid_group(tuple([get_card(CLUBS, THREE), get_card(HEARTS, THREE), get_card(SPADES, THREE), get_card(DIAMONDS, THREE), get_card(CLUBS, FOUR)]), FOUR)
    True
    >>> is_valid_group(tuple([get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE), get_card(SPADES, FIVE)]), FIVE)
    False
    """
    num_cards = len(cards)
    if num_cards < 3:
        return False
        
    num_wildcards, cards_list = remove_wildcards_from_hand(cards, wildcard_rank, num_cards)
    if num_cards == num_wildcards:
        return True
    
    return all_same_rank(tuple(cards_list))

@lru_cache(maxsize=LRU_CACHE_SIZE)
def is_valid_sequence(cards, wildcard_rank):
    """ (tuple<Card>, int) -> bool
    Checks if the given list of cards forms a valid sequence.
    A sequence is a set of three or more cards of the same suit with consecutive rank.
    A wildcard (card of the given wildcard rank) can fit in any sequence.
    >>> is_valid_sequence(tuple([]), KING)
    False
    >>> is_valid_sequence(tuple([get_card(HEARTS, TWO), get_card(HEARTS, THREE), get_card(HEARTS, FOUR)]), KING)
    True
    >>> is_valid_sequence(tuple([get_card(HEARTS, TWO), get_card(HEARTS, THREE), get_card(HEARTS, TEN)]), KING)
    False
    >>> is_valid_sequence(tuple([get_card(HEARTS, TWO), get_card(HEARTS, FOUR), get_card(HEARTS, TEN)]), TEN)
    True
    >>> is_valid_sequence(tuple([get_card(HEARTS, TWO), get_card(HEARTS, FIVE), get_card(HEARTS, TEN)]), TEN)
    False
    >>> is_valid_sequence(tuple([get_card(HEARTS, TWO), get_card(HEARTS, THREE), get_card(HEARTS, TEN)]), TEN)
    True
    >>> is_valid_sequence(tuple([get_card(SPADES, THREE), get_card(SPADES, JACK), get_card(SPADES, KING)]), THREE)
    True
    >>> is_valid_sequence(tuple([get_card(CLUBS, NINE), get_card(CLUBS, JACK), get_card(CLUBS, JACK)]), THREE)
    False
    >>> is_valid_sequence(tuple([get_card(CLUBS, NINE), get_card(CLUBS, JACK), get_card(CLUBS, JACK)]), JACK)
    True
    >>> is_valid_sequence(tuple([get_card(CLUBS, NINE), get_card(CLUBS, JACK), get_card(CLUBS, JACK), get_card(CLUBS, KING)]), JACK)
    False
    >>> is_valid_sequence(tuple([get_card(CLUBS, NINE), get_card(CLUBS, JACK), get_card(CLUBS, JACK), get_card(CLUBS, QUEEN)]), JACK)
    True
    >>> is_valid_sequence(tuple([get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE)]), FIVE)
    False
    >>> is_valid_sequence(tuple([get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE)]), FIVE)
    False
    >>> is_valid_sequence(tuple([get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE), get_card(SPADES, FIVE)]), FIVE)
    False
    """    
    num_cards = len(cards)
    if num_cards < 3:
        return False
        
    num_wildcards, cards_list = remove_wildcards_from_hand(cards, wildcard_rank, num_cards)
        
    if num_cards == num_wildcards:
        return True
    
    if not all_same_suit(tuple(cards_list)):
        return False

    # determine amount of gap in sequence, if any
    i = 1
    gaps = 0
    cards_list.sort()
    num_cards = len(cards_list)
    while i < num_cards:
        if get_rank(cards_list[i]) == get_rank(cards_list[i-1]):
            # can't have two cards of same rank in a sequence if they are not wildcards
            return False
        if get_rank(cards_list[i]) != get_rank(cards_list[i-1])+1:
            gaps += (get_rank(cards_list[i]) - get_rank(cards_list[i-1])) - 1
        i += 1
    
    return gaps <= num_wildcards # check if we can fill the gaps with wildcards

def arrangement_to_string(arrangement):
    s = ''
    i = 1
    for seq in arrangement:
        s += str(i) + "\t" + hand_to_string(seq) + "\n"
        i += 1
    return s

def equal_or_less_occurrences(elements, nested_tuple):
    for element in set(elements):
        x_count = elements.count(element)
        nested_count = 0
        for tup in nested_tuple:
            nested_count += tup.count(element)
            if nested_count > x_count:
                return False
    return True

@lru_cache(maxsize=LRU_CACHE_SIZE)
def get_arrangement(hand, wildcard_rank):
    """ (tuple<Card>, RANK) -> tuple<tuple<Card>>
    
    The two 3's and two wildcards will be put into a group of four Three's.
    >>> hand = tuple([get_card(CLUBS, TWO), get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE), get_card(SPADES, FIVE)])
    >>> wildcard_rank = FIVE
    >>> solution = ((get_card(CLUBS, THREE), get_card(CLUBS, THREE), get_card(CLUBS, FIVE), get_card(SPADES, FIVE)),)
    >>> get_arrangement(hand, wildcard_rank) == solution
    True
    """
    #print("is_valid_arrangement", is_valid_arrangement.cache_info())
    #print("is_valid_group", is_valid_group.cache_info())
    #print("is_valid_sequence", is_valid_sequence.cache_info())
    #print("remove_wildcards_from_hand", remove_wildcards_from_hand.cache_info())
    #print("get_arrangement", get_arrangement.cache_info())
    len_hand = len(hand)
    if len_hand < 3:
        return []
    
    valid_combinations = set()
    stop = False
    for group_length in range(len_hand, 2, -1):
        for combination in combinations(hand, group_length):
            if is_valid_sequence(combination, wildcard_rank) or is_valid_group(combination, wildcard_rank):
                valid_combinations.add((combination, group_length))
                if group_length == len_hand: # don't keep looking if we found a combo for entire hand
                    stop = True
                    break
        if stop:
            break
    
    if len(valid_combinations) == 0:
        return tuple()
            
    # find optimal combination of groups and sequences
    cur_max_arrangements = []
    cur_max_arranged_cards = 0
    max_possible_arrangements = min(len(valid_combinations), len_hand // 3)
    for num_sequences in range(max_possible_arrangements, 0, -1):
        for arrangement in combinations(valid_combinations, num_sequences):
            arrangement, lengths = zip(*arrangement)
            if arrangement in cur_max_arrangements:
                continue
            arrangement_length = sum(lengths)
            if arrangement_length > len_hand or arrangement_length < cur_max_arranged_cards:
                continue
            if not equal_or_less_occurrences(hand, arrangement):
                continue
            if arrangement_length > cur_max_arranged_cards:
                cur_max_arranged_cards = arrangement_length
                cur_max_arrangements = [arrangement]
            elif arrangement_length == cur_max_arranged_cards:
                cur_max_arrangements.append(arrangement)
    if cur_max_arranged_cards == len_hand:
        best_arrangement = cur_max_arrangements[0]
    else:
        best_arrangement = get_min_penalty_arrangement(tuple(cur_max_arrangements), hand)

    return best_arrangement

def get_min_penalty_arrangement(cur_max_arrangements, hand):
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
    return best_arrangement

if __name__ == "__main__": 
    doctest.testmod()