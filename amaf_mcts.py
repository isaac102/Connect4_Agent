import time
import math
import random
def printer(State, cp_time):
        print(State)

def mcts_policy(cp_time,  alpha = 0, rave = None, use_exp = 1, amaf_debug = 0):
    def pt(State):
        imp_tree = {} #imp_tree[State] = (times visited, total points)
        amaf_imp_tree = {} #amaf_imp_tree[move_tuple] = (times visited, total pionts)
        
        #returns the score given by the ucb formula for a node
        def ucb_score_of_move(move, parent, alpha=alpha, rave=rave):
            score = None
            p1 = (parent.actor() == 0)
            state = parent.successor(move)
            if(state not in imp_tree or imp_tree[state][0] == 0):
                #not in tree, or never been visited, should be a top choice
                imp_tree[state] = [0,0]
                amaf_imp_tree[state] = [0,0]
                score = float("inf") if p1 else -1 * float("inf")
            else:
                state_node = imp_tree[state]
                #has been visited before, so we apply ucb formula
                payoff = state_node[1]/state_node[0]
                exploration = math.sqrt(
                       2 * math.log(imp_tree[parent][0])/state_node[0]
                        )
                if(p1):
                    score = payoff + exploration
                else:
                    score = payoff - exploration
                #amaf version
                state_node = amaf_imp_tree[state]
                #has been visited before, so we apply ucb formula
                payoff = state_node[1]/state_node[0]
                exploration = math.sqrt(
                       2 * math.log(imp_tree[parent][0])/state_node[0]
                        )
                #calculate ucb score by using ucb formula, or by excluding the exploration term depending on initial call to function, used to test various cases
                if(p1):
                    amaf_score = payoff + exploration * use_exp
                else:
                    amaf_score = payoff - exploration * use_exp
                #depending on if rave or alpha amaf, calculate combined score
                if(rave == None):
                    return score * (1-alpha) + amaf_score * alpha
                else:
                    param = max(0, (rave - imp_tree[state][0])/rave)
                    return score * (1-param) + amaf_score * param
            return score


        #returns a leaf node to explore, and the path taken to get there
        def find_leaf(State, history = [], rejected = [], alpha = alpha, rave = rave):
            p1 = (State.actor() == 0)
            node = imp_tree[State]
            children = State.get_actions()
            best = []
            sc = -1 * float("inf") if (p1) else float("inf")
            for child in children:
                #will return the score with a-amaf or rave
                ucb_score = ucb_score_of_move(child, State, alpha, rave)
                if(p1):
                    if(ucb_score > sc):
                        sc = ucb_score
                        best = [child]
                    elif(ucb_score == sc):
                        best.append(child)
                else:
                    if(ucb_score < sc):
                        sc = ucb_score 
                        best = [child]
                    elif(ucb_score == sc):
                        best.append(child)

            history.append(State)
            chosen = random.choice(best)
            best.remove(chosen)
            for rej in best:
                rejected.append((tuple(rej), State.successor(rej)))
            chosen_state = State.successor(chosen)
            chosen_state_node = imp_tree[chosen_state]
            if(chosen_state_node[0] == 0 or chosen_state.is_terminal()):
                #the best state is not visited, or is terminal, so no need to go any further
                return [chosen_state, history, chosen, rejected]
            else:
                #state has been visited an is non terminal, so we must pick a child
                res = find_leaf(chosen_state, history, rejected)
                res[-1] += rejected
                return res


        #explore a node: if the node is terminal, return value of state. if node is nonterminal, play randomly until terminal then return value
        def explore(State):
            #play randomly until terminal state
            st = State
            moves_seen = set()
            while(not st.is_terminal()):
                st_move = random.choice(st.get_actions())
                moves_seen.add((st_move[0], st_move[1]))
                st = st.successor(st_move)
            return (st.payoff(), moves_seen)

        #given a value from a state, propagate the value
        def propagate(State, value, history):
            history.append(State)
            for st in history:
                imp_tree[st][0] += 1
                amaf_imp_tree[st][0] += 1
                imp_tree[st][1] += value
                amaf_imp_tree[st][1] += value
        def amaf_propagate(value, rejected, moves_seen):
            to_update = []
            for rej in rejected:
                if(rej[0] in moves_seen):
                    to_update.append(rej[1])
            for st in to_update:
                #print("made update")
                if(amaf_debug):
                    print(st, "was",  amaf_imp_tree[st])
                amaf_imp_tree[st][0] += 1
                amaf_imp_tree[st][1] += value
                if(amaf_debug):
                    print(st,"is now", amaf_imp_tree[st])
            return to_update
          
        
        imp_tree[State] = [0,0]
        amaf_imp_tree[State] = [0,0]
        val, moves_seen  = explore(State)
        propagate(State, val, [])
        t_end = time.time() + cp_time
        the_same = 0 
        count = 0
        while time.time() < t_end:
            leaf, history, choice, rejected = find_leaf(State, [], [])
            
            #leaf2, history2, choice2, rejected2 = find_leaf(State, [], [])
            #count += 1
            #if(leaf == leaf2):
            #    the_same += 1
            #print(leaf, leaf2, leaf == leaf2)
            rejected = set(rejected)
            val, moves_seen = explore(leaf)
            propagate(leaf, val, history)
            amaf_updated = amaf_propagate(val, rejected, moves_seen)
        #print("fraction the same: ", the_same/count)
        p1 = State.actor() == 0
        chosen = []
        best = -1 * float("inf")
        scal = 1 if p1 else -1
        for c_child in State.get_actions():
            child = State.successor(c_child)
            if(child not in imp_tree or imp_tree[child][0] == 0):
                continue
            c_arr = imp_tree[child]
            
            value = scal * c_arr[1]/c_arr[0] if not c_arr[0] == 0 else float("inf")
            if(value > best):
                chosen = [c_child]
                best = value
            elif(value == best):
                chosen.append(c_child)
        if(len(chosen) == 0):
            if(not len(State.get_actions()) == 0):
                return State.get_actions()[0]
            return None

        choice = random.choice(chosen)
        return choice

    return pt


