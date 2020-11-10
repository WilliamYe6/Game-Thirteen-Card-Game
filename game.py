from card import *
from arrangement import *
from random import seed, shuffle
from collections import defaultdict
#seed(1337)
MAX_NUM_TURNS_PER_PLAYER = 3000

def calculate_winner(points):
    winners = []
    min_score = min(points)
    for i in range(len(points)):
        if points[i] == min_score:
            winners.append(i)
    return winners

def calculate_round_points(hand):
    points = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1]
    score = 0
    for card in hand:
        score += points[RANKS.index(get_rank(card))]
    return score

def get_starting_hands(deck, num_players, num_cards):
    hands = []
    for i in range(num_players):
        hands.append([]) # create empty hand for each player
        for j in range(num_cards):
            hands[-1].append(deck.pop()) # add specified num cards to each player
    return hands

def round_end(player_names, hands, current_points):
    round_points = []
    for hand in hands:
        round_points.append(calculate_round_points(hand))
    
    print("Round points (the lower the better):")
    for player, score in zip(player_names, round_points):
        print(player, "\t", score)
    
    for i in range(len(round_points)):
        current_points[i] += round_points[i]
    
    print("Total points (the lower the better):")
    for player, score in zip(player_names, current_points):
        print(player, "\t", score)

def player_turn(player, player_name, player_index, hand, discard_pile, stock, winning_player, picked_up_discard_cards, wildcard_rank, num_turns_this_round):
    assert len(discard_pile) > 0

    print("Player " + str(player_index) + " (" + player_name + ")'s turn")
    #print("Hand:", hand_to_string(hand))
    assert len(hand) > 0
    print("Top card of discard pile:", card_to_string(discard_pile[-1]))
    
    # Step 1: Draw
    draw_location = player.draw(hand[:], discard_pile[-1], winning_player>-1, picked_up_discard_cards, player_index, wildcard_rank, num_turns_this_round)
    assert draw_location in ['stock', 'discard']

    if draw_location == 'stock':
        if len(stock) == 0:
            print("Reshuffling stock pile")
            stock.clear()
            stock.extend(discard_pile)
            shuffle(stock)
            discard_pile.clear()
        hand.append(stock.pop())
    elif draw_location == 'discard':
        hand.append(discard_pile.pop())
        picked_up_discard_cards[player_index].append(hand[-1])

    print("Player draws from " + draw_location + ". They draw the", card_to_string(hand[-1]))

    # Step 2: Discard
    card = player.discard(hand[:], winning_player>-1, picked_up_discard_cards, player_index, wildcard_rank, num_turns_this_round)
    assert card in hand
    hand.remove(card)
    discard_pile.append(card)
    print("Player discards the", card_to_string(card))

    # Step 3: Check if player has gone out
    arrangement = get_arrangement(hand[:], wildcard_rank)
    if is_valid_arrangement(arrangement, hand, wildcard_rank):
        print("Player announced they have gone out.")
        print("  Their hand contains:", hand_to_string(hand))
        print("  They have arranged their hand as follows:\n", arrangement_to_string(arrangement))
        return True
    
    return False

def main(players, display_gui):
    if display_gui:
        import gui
        screen = gui.start()
    
    player_names = []
    for player in players:
        player_names.append(player.__file__.split('/')[-1])
    
    print("Starting game.")
    print("Players:", player_names)
    max_turns_per_round = MAX_NUM_TURNS_PER_PLAYER * len(players)
    
    total_scores = [0] * len(players)
    for rnd in range(1, 12): # 11 rounds
        print("\n\nStarting round " + str(rnd) + " (" + str(rnd+2) + " cards per player)")
        
        deck = get_deck() + get_deck()
        shuffle(deck)
        
        # deal cards to each player, removing them from deck
        hands = get_starting_hands(deck, len(players), rnd+2)
        
        stock = deck # rest of cards form deck
        discard_pile = [stock.pop()] # turn up one card from stock
                
        wildcard_rank = rnd   # round 1 = THREE (1); round 2 = FOUR (2), etc.
        
        winning_player = -1
        picked_up_discard_cards = []
        for i in range(len(players)):
            picked_up_discard_cards.append([])

        cur_player = 0
        num_turns_this_round = 0
        while True: # give each person a turn until round ends
            #print("Stock", hand_to_string(stock))
            #print("Discard pile", hand_to_string(discard_pile))
            
            if cur_player == winning_player:
                # play has come back around, so end the round
                print("Round over.")
                break
            elif num_turns_this_round > max_turns_per_round:
                print("Number of turns exceeded limit, ending round due to timeout.")
                break
            
            print("\n\nRound", rnd, "turn", num_turns_this_round, "(wildcard: " + RANKS_STR[wildcard_rank] + ")")
            player_won = player_turn(players[cur_player], player_names[cur_player], cur_player, hands[cur_player], discard_pile, stock, winning_player, picked_up_discard_cards, wildcard_rank, num_turns_this_round)
            #input("End of turn. Press [return] to continue.")
            if display_gui:
                gui.display(screen, hands, discard_pile[-1], total_scores)
            if player_won and winning_player == -1: # player arranged all their cards and no one has gone out yet
                print("Player has gone out. Giving everyone a final turn.")
                hands[cur_player] = []
                winning_player = cur_player # end the game at the winning player's next turn
            
            cur_player = (cur_player + 1) % len(players)
            num_turns_this_round += 1
        
        # round end
        print("\n\nEnd of round " + str(rnd) + ". Arranging everyone's hands.")
        input("Press [return] to continue.")
        
        # arrange players' hands as much as possible
        for cur_player in range(len(players)):
            arrangement = get_arrangement(hands[cur_player][:], wildcard_rank)
            # remove all arranged cards from their hand
            for seq in arrangement:
                for card in seq:
                    hands[cur_player].remove(card) # removes first matching element
        
        # tally points of non-arranged cards
        round_end(player_names, hands, total_scores) # modifies total scores
        if display_gui:
            gui.display(screen, hands, total_scores)
        else:
            input("Press [return] to continue.")
    
    # determine winner
    winner = calculate_winner(total_scores)
    print("Player", winner, "has won!")
    if display_gui:
        gui.stop()
