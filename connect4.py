import copy
class ConnectFour:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.num_per_col = [0,0,0,0,0,0,0]
        self.current_player = 0  # Player 1 always starts
        self.terminal = False
        self.reward = None
        self.children = {}
        
        #print("initialized")

    def actor(self):
        return self.current_player

    def get_actions(self):
        return self.get_available_moves()

    def is_legal(self, move):
        return (move in self.get_available_moves())
        
    def human_successor(self, move):
        move = [5-self.num_per_col[move],move]
        return self.successor(move)

    def successor(self, move):
        mkey = (move[0],move[1])
        if(mkey in self.children):
            return self.children[mkey]
        succ = ConnectFour()
        succ.board = copy.deepcopy(self.board)
        succ.num_per_col = self.num_per_col.copy()
        succ.current_player = self.current_player
        succ.terminal = self.terminal
        succ.reward = self.reward
        #print("abt to move from successor func")
        succ.move(move)
        self.children[mkey] = succ
        return succ

    def is_terminal(self):
        return self.terminal

    def payoff(self):
        if(not self.terminal):
            print("Not a terminal state. No reward.")
            return None
        else:
            return self.reward
 
    #print the game board for visual use
    def print_board(self):
        spaces = ['0', '1','2','3','4','5','6']
        bot = ['-','-','-','-','-','-','-']
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print(' ' + ' '.join(bot))
        print(' ' + ' '.join(spaces))

    def get_available_cols(self):
        available = []
        for i in range(7):
            if(self.num_per_col[i] < 6):
                available.append(i)
            
        return available

    def get_available_moves(self):
        cols = self.get_available_cols()
        moves = []
        for col in cols:
            moves.append([5-self.num_per_col[col],col])
        return moves

    def move(self, move):
        if(self.board[move[0]][move[1]] != ' '):
            print("Illegal move!")
            return -1
        self.board[move[0]][move[1]] = 'X' if self.current_player == 0 else 'O'
        self.num_per_col[move[1]] += 1
        won = self.winning_move(move)
        if(won):
            self.terminal = 1
            self.reward = 1 if self.current_player == 0 else -1
        elif(len(self.get_available_cols()) == 0):
            self.terminal = 1
            self.reward = 0
        self.current_player = 1 - self.current_player
        return 0

    def winning_move(self, move):
        row, col = move
        #check if won horizontal, vertical, diag y=-x, diag y=x
        directions = [(0, 1),  (1, 0), (1, 1), (-1, 1)]
        piece = 'X' if self.current_player == 0 else 'O'
        for change_r, change_c in directions:
            count = 0
            for n in range(-4,4):
                r = row + change_r * n
                c = col + change_c * n
                if r < 0 or r > 5 or c < 0 or c > 6:
                    count = 0
                elif self.board[r][c] != piece:
                    count = 0
                else:
                    count += 1
                    #print("here with r,c", r, c)
                if count == 4:
                    #print("won", move)
                    #print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                    #self.print_board()
                    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    self.terminal = True
                    return True
       # print("now won yet")
        return False
    
    def run_player_game(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        while True:
            self.print_board()
            print(self.get_available_moves())
            col = int(input(f"Player {self.current_player}, choose a column (0-6): "))
            
            mv =self.move([5-self.num_per_col[col],col]) 
            if(mv == -1 or col < 0 or col > 6):
                print("close on move error")
                continue
                return
            if(self.terminal):
                self.print_board()
                if(self.reward == 1):
                    print("Game over! Player 1 won")
                elif(self.reward == -1):
                    print("Game over! Player 2 won")
                else:
                    print("its a tie :|")
                return 0
            
    
#initialize game
#game = ConnectFour()
#game.run_player_game()  
#print(game.get_available_moves())
