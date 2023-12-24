import time
import math
import random
def printer(State, cp_time):
        print(State)

#plan - until run out of time, explore leaf chosen by ucb
#once time has run out, select best move (best child)
#functions needed: find_leaf:finds the best node to explore by using ucb
#explore leaf: explores the node selected and propegates back the value

#refoctor for readability - do not store children in imp_tree, store action to child

def mcts_policy(cp_time):
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    def pt(State):
        imp_tree = {} #imp_tree[State] = (times visited, total points)
        #print(State.actor())
        
        #returns the score given by the ucb formula for a node
        def ucb_score_of_move(move, parent):
            score = None
            p1 = (parent.actor() == 0)
            state = parent.successor(move)
            if(state not in imp_tree or imp_tree[state][0] == 0):
                #not in tree, or never been visited, should be a top choice
                imp_tree[state] = [0,0]
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
            return score

        #returns a leaf node to explore, and the path taken to get there
        def find_leaf(State, history = []):

            p1 = (State.actor() == 0)
            #if(State not in imp_tree):
            #    print("here")
                #state is not in the tree, should only happen to first call with root node
            #    imp_tree[State] = [0,0]
            #    return [State, history, None]
            #else:
                #the state is in the tree, and must be already visited and nonterminal
            node = imp_tree[State]
            children = State.get_actions()
            best = []
            sc = -1 * float("inf") if (p1) else float("inf")
            for child in children:
                ucb_score = ucb_score_of_move(child, State)
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
            chosen_state = State.successor(chosen)
            #print(imp_tree)
            chosen_state_node = imp_tree[chosen_state]
            if(chosen_state_node[0] == 0 or chosen_state.is_terminal()):
                #the best state is not visited, or is terminal, so no need to go any further
                #print(chosen, " was the chosen one")
                return [chosen_state, history, chosen]
            else:
                #state has been visited an is non terminal, so we must pick a child
                #print(chosen, " was the non_terminal chosen one", chosen_state_node)
                return find_leaf(chosen_state, history)



        #explore a node: if the node is terminal, return value of state. if node is nonterminal, play randomly until terminal then return value
        def explore(State):
            #play randomly until terminal state
            st = State
            #print("start explore")
            #st.print_board()
            while(not st.is_terminal()):
                st_move = random.choice(st.get_actions())
                st = st.successor(st_move)
                #st = random.choice([st.successor(x) for x in st.get_actions()])
                #st.print_board()
                #print(st.is_terminal())
            return st.payoff()

        #given a value from a state, propegate the value
        def propegate(State, value, history):
            #print(len(history))
            history.append(State)
            for st in history:
                imp_tree[st][0] += 1
                imp_tree[st][1] += value
            #print("propegated state", State, imp_tree[State])

        #random baseline
        #return random.choice(State.get_actions())
        
        #print("init root")
        #initialize root of tree
        imp_tree[State] = [0,0]
        #print("set imp tree")
        val = explore(State)
        #print("got val")
        propegate(State, val, [])
        #print("played 1 game")
        t_end = time.time() + cp_time
        while time.time() < t_end:
            #print("run cycle")
            leaf, history, choice = find_leaf(State, [])
            #print("found leaf")
            val = explore(leaf)
            #print("val is ", val)
            propegate(leaf, val, history)
            #print(choice, imp_tree[leaf],"was actually the chosen one")

        #print("-----------------------")
        #print(State)
        #print(State.actor())
        #for ac in State.get_actions():
        #    print(ac)
        #    st = imp_tree[State.successor(ac)]
        #    print(st[1])
        #    print(st[0])

        p1 = State.actor() == 0
        #print(State.successor(State.get_actions()[0]).actor() == State.actor(), "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        chosen = []
        best = -1 * float("inf")
        scal = 1 if p1 else -1
        for c_child in State.get_actions():
            child = State.successor(c_child)
            if(child not in imp_tree or imp_tree[child][0] == 0):
                #print("fine")
                continue
            #    print("should not occur*************************************")
            #    print("*************************************")
            #    print("************************************************************************************************")
            #    scal.get_successor()
            #    continue
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
        #counts_vals = [(x, "has count and ratio values ", 
        #                imp_tree[State.successor(x)][0], 
        #                imp_tree[State.successor(x)][1], 
        #                imp_tree[State.successor(x)][1]/imp_tree[State.successor(x)][0]
        #                ) for x in State.get_actions()]
        #print(State.actor())
        #print(counts_vals)
        #print(choice)
        #print(imp_tree[State][0])
        return choice

    return pt


