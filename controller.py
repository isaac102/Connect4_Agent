from connect4 import ConnectFour
#print("c0")
import random
import sys
import mcts
import amaf_mcts
import time


#game = ConnectFour()
#moves = game.get_actions()
#game2 = game.successor(moves[0])
#game.move([5,3])
#game.move([5,4])
#game.print_board()
#game2.print_board()
#print(game.actor())
#print(game2.actor())
#game2.run_player_game()
  
def get_human_play(position):
    col = int(input(f"here Player {position.current_player}, choose a column (0-6): "))
    move = [5-position.num_per_col[col],col]
    #position = position.successor(move)
    if(position == -1 or col < 0 or col > 6):
        print("close on move error")
        return -1
    return move

def get_mcts_play(policy, position, player_time):
    start = time.time()
    move = policy(position)
    position = position.successor(move)
   # print(start, time.time(), player_time)
    player_time = max(player_time, time.time() - start)

    return (position, player_time)

tests = []
def tester(policy0_params, policy1_params, num_iter, human = 0, amaf_debug = 0):

    wins = {"mc_policy":0, "mc_policy1":0, "tie":0}
    for i in range(num_iter):
        position = ConnectFour()
        comp_player = random.randint(0,1)
        player0 = "mc_policy" if not comp_player else "mc_policy1"
        player1 = "mc_policy" if comp_player else "mc_policy1"

        if(human == 0):
            if(amaf_debug):
                mc_policy = amaf_mcts.mcts_policy(policy0_params[0], policy0_params[1], policy0_params[2], amaf_debug = 1)
                mc_policy1 = amaf_mcts.mcts_policy(policy1_params[0], policy1_params[1], policy1_params[2], amaf_debug = 1)
            else:
                mc_policy = amaf_mcts.mcts_policy(policy0_params[0], policy0_params[1], policy0_params[2])
                mc_policy1 = amaf_mcts.mcts_policy(policy1_params[0], policy1_params[1], policy1_params[2])
        elif(human == 1):
            mc_policy = amaf_mcts.mcts_policy(policy0_params[0], policy0_params[1], policy0_params[2])
            mc_policy1 = get_human_play
        elif(human == 2):
            mc_policy = get_human_play
            mc_policy1 = get_human_play

        p1_time = 0.0
        p0_time = 0.0

        while not position.is_terminal():
            if(human):
                position.print_board()
            if position.actor() == comp_player:
                position, p0_time = get_mcts_play(mc_policy, position, p0_time)
            else:
                position, p1_time = get_mcts_play(mc_policy1, position, p1_time)

        if(human):
            position.print_board()
        if(position.reward == 1):
            wins[player0] += 1
            if(human):
                print(f"player0:{player0} won")
        elif(position.reward == -1):
            wins[player1] += 1
            if(human):
                print(f"player1: {player1} won")
        else:
            wins["tie"] += 1
            if(human):
                print("tie")
        #print(f"{player0} time is {p0_time} and {player1} time is {p1_time}")


    #print(wins)
    tests.append(((policy0_params, policy1_params, num_iter), wins))
    return ((policy0_params, policy1_params, num_iter), wins)

#
#for i in range(4,15):
#    policy0_params = (.1, 0, None)
#    policy1_params = (.1, .5, i * 2)
#    tester(policy0_params, policy1_params, 1000)
#
#policy0_params = (.1, 0, None)
#policy1_params = (.1, .5, None)
#tester(policy0_params, policy1_params, 1000)
#
#policy1_params = (.1, .8, None)
#tester(policy0_params, policy1_params, 1000)
#
#policy1_params = (.1, .3, None)
#tester(policy0_params, policy1_params, 50)


#
#for t in tests:
#    print(t[0])
#    print(t[1])
#    print(t[1]["mc_policy1"]/(t[1]["mc_policy"] + t[1]["mc_policy1"] + t[1]["tie"]))



#print(tests)

#.01 per move mcts vs .7 a-amaf 1,000 times: {mcts:508 amaf:489}
#.01 per move mcts vs .5 a-amaf 1,000 times: {mcts:496 amaf:501}
#.05 per move mcts vs .5 a-amaf 1,000 times: {mcts:481 amaf:500}
#.1 per move mcts vs .5 a-amaf 500 times: {mcts:249 amaf:236}
#.1 per move mcts vs .5 rave 5 500 times: {mcts:234 amaf:256}
#percentages for mcts agains rave, .1 per move, 100 iter, percent win for rave at levels 2:18 (.46,.53,.42,.47,.48,.5,.43,.55,.55)


#overnight runs of 1000 iter 
#1 second per reg-464 a-amaf .8 -487 tie 49
#1 second per reg-493 a-amaf .5 -457 tie 50
#1 second per reg-480 a-amaf .3 -474 tie 50


#((0.1, 0, None), (0.1, 0.5, 8), 1000)
#{'mc_policy': 452, 'mc_policy1': 505, 'tie': 43}
#0.505
#((0.1, 0, None), (0.1, 0.5, 10), 1000)
#{'mc_policy': 470, 'mc_policy1': 493, 'tie': 37}
#0.493
#((0.1, 0, None), (0.1, 0.5, 12), 1000)
#{'mc_policy': 477, 'mc_policy1': 483, 'tie': 40}
#0.483
#((0.1, 0, None), (0.1, 0.5, 14), 1000)
#{'mc_policy': 496, 'mc_policy1': 462, 'tie': 42}
#0.462
#((0.1, 0, None), (0.1, 0.5, 16), 1000)
#{'mc_policy': 467, 'mc_policy1': 490, 'tie': 43}
#0.49
#((0.1, 0, None), (0.1, 0.5, 18), 1000)
#{'mc_policy': 527, 'mc_policy1': 442, 'tie': 31}
#0.442
#((0.1, 0, None), (0.1, 0.5, 20), 1000)
#{'mc_policy': 467, 'mc_policy1': 491, 'tie': 42}
#0.491
#((0.1, 0, None), (0.1, 0.5, 22), 1000)
#{'mc_policy': 471, 'mc_policy1': 484, 'tie': 45}
#0.484
#((0.1, 0, None), (0.1, 0.5, 24), 1000)
#{'mc_policy': 464, 'mc_policy1': 498, 'tie': 38}
#0.498
#((0.1, 0, None), (0.1, 0.5, 26), 1000)
#{'mc_policy': 492, 'mc_policy1': 476, 'tie': 32}
#0.476
#((0.1, 0, None), (0.1, 0.5, 28), 1000)
#{'mc_policy': 494, 'mc_policy1': 458, 'tie': 48}
#0.458
#


















