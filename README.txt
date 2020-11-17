Hello! 

We wrote three helper functions. The first (complete_arragement) allows us to sabotage other players by 
not discarding cards that may complete other players' arrangement(s). The second helper function (second_best_draw)
allows us to compute the cards that we should pick up if there is no card available that would form an arrangement. 
The third (and final) helper function helps us caluclate the point value of each card; we used it in the draw function. 

In the discard function, we lowered the penalty points of cards that may complete other players' hand so that AI 
will not discard it. 

When coding, we prioritized keeping cards that could form a group rather than sequences as we figured that there is a 
higher probability of us drawing cards that form a group. 

We decided to use 8 as a cut-off point as it cuts the deck in 2; cards higher than that have higher penalty points 
and vice versa. The Ace is an exception (although it is a 'higher' card, it has lower penalty points). 

Happy testing and may the odds be ever in our favor :)
