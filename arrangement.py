import math
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
    cards = []
    for seq in arrangement:
        if not is_valid_group(seq, wildcard_rank) and not is_valid_sequence(seq, wildcard_rank):
            return False
        
        cards.extend(seq)
    
    return equal_occurrences(hand, cards)

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
    """
    assert type(cards) is tuple
    if len(cards) < 3:
        return False

    if (cards, wildcard_rank) not in valid_groups:
        group_rank = get_rank(cards[0])
        result = True
        for card in cards[1:]:
            card_rank = get_rank(card)
            if card_rank != group_rank and card_rank != wildcard_rank:
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
    >>> is_valid_sequence([get_card(HEARTS, TWO), get_card(HEARTS, THREE), get_card(HEARTS, FOUR)], KING)
    True
    >>> is_valid_sequence([get_card(HEARTS, TWO), get_card(HEARTS, THREE), get_card(HEARTS, TEN)], KING)
    False
    >>> is_valid_sequence([get_card(HEARTS, TWO), get_card(HEARTS, THREE), get_card(HEARTS, TEN)], TEN)
    True # the ten will become a four as it is a wildcard
    >>> is_valid_sequence([])
    False
    """
    assert type(cards) is tuple
    if (cards, wildcard_rank) not in valid_sequences:
        cards_list = list(cards)
        result = True
        
        num_wildcards = 0
        for i in range(len(cards_list)-1, -1, -1):
            card = cards_list[i]
            if get_rank(card) == wildcard_rank:
                num_wildcards += 1
                cards_list.remove(card)
    
        if len(cards_list) < 3-num_wildcards:
            result = False
        elif not all_same_suit(cards_list):
            result = False
        else:
            # determine amount of gap in sequence, if any
            i = 1
            gaps = 0
            while i < len(cards_list):
                if get_rank(cards_list[i]) != get_rank(cards_list[i-1])+1:
                    gaps += (get_rank(cards_list[i]) - get_rank(cards_list[i-1])) + 1
                i += 1
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
            element_counts[elements] = Counter(elements)
        if nested_tuple not in nested_tuple_counts:
            nested_tuple_counts[nested_tuple] = Counter(chain(*nested_tuple))
        
        e_cts = element_counts[elements]
        nt_cts = nested_tuple_counts[nested_tuple]
        
        if any(nt_cts[x] > e_cts[x] for x in elements):
            result = False
        
        occurrences[(elements, nested_tuple)] = result
    return occurrences[(elements, nested_tuple)]

def count_elements(nested_list):
    num = 0
    for x in nested_list:
        for y in x:
            num += 1
    return num

best_arrangements = {}
def get_arrangement(hand, wildcard_rank):
    if len(hand) < 3:
        return []
    
    hand = hand[:]
    hand.sort()
    hand_t = tuple(hand)
    if (hand_t, wildcard_rank) in best_arrangements:
        return best_arrangements[(hand_t, wildcard_rank)]
    
    valid_combinations = set()
    for group_length in range(3, len(hand)+1):
        for combination in combinations(hand, group_length):
            if is_valid_group(combination, wildcard_rank) or is_valid_sequence(combination, wildcard_rank):
                valid_combinations.add(combination)
        
    if len(valid_combinations) == 0:
        best_arrangements[(hand_t, wildcard_rank)] = []
        return []
    
    # find optimal combination of groups and sequences
    cur_max_arrangements = []
    cur_max_arranged_cards = 0
    max_possible_arrangements = min(len(valid_combinations), len(hand) // 3)
    for num_sequences in range(max_possible_arrangements, -1, -1):
        for arrangement in combinations(valid_combinations, num_sequences):
            if arrangement not in cur_max_arrangements and equal_or_less_occurrences(hand_t, arrangement):
                num_cards_in_sequence = count_elements(arrangement)
                if num_cards_in_sequence > cur_max_arranged_cards:
                    cur_max_arranged_cards = num_cards_in_sequence
                    cur_max_arrangements = [arrangement]
                elif num_cards_in_sequence == cur_max_arranged_cards:
                    cur_max_arrangements.append(arrangement)
    
    if cur_max_arranged_cards == len(hand):
        best_arrangement = cur_max_arrangements[0]
    else:
        min_point_val = math.inf
        best_arrangement = None
        points = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1]
        for arrangement in cur_max_arrangements:
            unarranged_cards = hand[:]
            for seq in arrangement:
                for card in seq:
                    unarranged_cards.remove(card)
            point_value = 0
            for card in unarranged_cards:
                point_value += points[RANKS.index(get_rank(card))]
            if point_value < min_point_val:
                min_point_val = point_value
                best_arrangement = arrangement
    assert best_arrangement is not None
            
    best_arrangements[(hand_t, wildcard_rank)] = best_arrangement
    return best_arrangement