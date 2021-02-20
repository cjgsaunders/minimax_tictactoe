import random, time
from math import inf as infinity

count = 0

class Agent:
    def __init__(self, symbol, opponent):  #Init params shared by all players
        self.symbol = symbol
        self.opponent = opponent

    def simple_move(self, state, level):
        """
        easy and medium use this to make a random move.
        :param state: the board
        :param level: the ai difficulty to be pritned
        """        
        random_move = random.choice(self.empty_cells(state))
        state[random_move[0]][random_move[1]] = self.symbol
        print(f'Making move level "{level}"')
        time.sleep(0.5)
        self.grid_draw(state)

    def valid_move(self, row, col, state):
        """
        A move is valid if the chosen cell is empty
        :param row: horizontal axis
        :param col: vertical axis
        :return: True if the board[row][col] is empty
        """
        if [row, col] in self.empty_cells(state):
            return True
        else:
            return False

    def empty_cells(self, state):
        """
        the first loop returns a row and its index   0 [' ', ' ', ' ']
        the second loops over the index to return the cell [0, ' ']
        this gives the row , col coords for the empty cell.
        """
        cells = []
        for row, index in enumerate(state):
            for col, cell in enumerate(index):
                if cell == " ":
                    cells.append([row, col])
        return cells

    def set_move(self, row, col, player, board_in):
        """
        Set the move on board, if the coordinates are valid
        :param row: horizontal axis
        :param col: vertical axis
        :param player: the current player
        """
        if self.valid_move(row, col, board_in):
            board_in[row][col] = player
            return True
        else:
            print(row,col, "error")
            return False

    def grid_draw(self, state): 
        """
        Draws the grid after a player makes a move.
        :param state: The current board state
        """ 
        print('---------')
        for i in range (3):       
            print(f"| {state[i][0]} {state[i][1]} {state[i][2]} |")
        print('---------')

    def draw(self, state):
        """
        checks to see if no more moves are possible
        :param state: the board state
        """
        if len(self.empty_cells(state)) == 0:
            return True
    
    def wins(self, state, player):
        """
        This function tests if a specific player wins. Possibilities:
        * Three rows    [X X X] or [O O O]
        * Three cols    [X X X] or [O O O]
        * Two diagonals [X X X] or [O O O]
        :param state: the state of the current board
        :param player: a symbol ("X" or "O")
        :return: True if the player wins
        """

        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        
        else:
            return False

    def game_won(self, state):
        """
        This function calls wins() twice with each mark to
        check for a terminal state and returns true if found.
        """
        return self.wins(state, "X") or self.wins(state, "O")

    def who_won(self, state):
        """
        This is called after the game has been won.
        Returns the winner to be printed.
        """
        return "X wins" if self.wins(state, "X") else "O wins" if self.wins(state, "O") else "Draw"

class Human(Agent):
    def __init__(self, symbol, opponent):
        super().__init__(symbol, opponent)

    def move(self, board_in): 
        """
        Checks to see if the game is over.
        Takes input from the user and checks for
        correctness.
        :param board_in: the current game board
        """
       
        if self.game_won(board_in) or self.draw(board_in):  
            return

        
   
        # Dictionary of valid moves
        move = -1
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }
    
        while True:
            coords = input('Enter the coordinates: ') # Checks the format (must be "number[space]number")
            coords = coords.replace(" ", "")
            if len(coords) != 2 or coords.isalpha():
                    print("You should enter numbers!")
            elif coords[0] not in "123" or coords[1] not in "123":# Must be in either 1, 2 or 3
                    print("out of range")
            else:
                row, col = int(coords[0]) - 1, int(coords[1]) - 1   # format to the propper grid
                if not self.valid_move(row,col, board_in):
                    print('This cell is occupied! Choose another one!')
                else:
                    self.set_move(row, col, self.symbol, board_in)
                    self.grid_draw(board_in)                
                    break    

class hard_AI(Agent):

    def __init__(self, symbol, opponent):
        super().__init__(symbol, opponent)

    def move(self, state):
        """
        It calls the minimax function if the depth < 9,
        else it choices a random coordinate.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        global count
        count = 0  # This tracks how many games are simulated
                
        move = self.minimax(state, 0, True)
        row, col = move[0], move[1]

        self.set_move(row, col, self.symbol, state)
        print(f'Making move level "hard"')
        time.sleep(0.5)
        self.grid_draw(state)
        #print(count)
        

    def evaluate(self, state):
        global count
        count = count+1
        """
        Heuristic function.
        :param state: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        if self.wins(state, self.symbol):
            score = +1
        elif self.wins(state, self.opponent):
            score = -1
        else:
            score = 0

        return score

    def minimax(self, state, depth, maximising):
        """
        AI function that choice the best move
        :param state: current state of the board
        :param depth: not used
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        moves_left = len(self.empty_cells(state))
        
        if maximising:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if moves_left == 0 or self.game_won(state):
            score = self.evaluate(state)
            return [-1, -1, score]

        for cell in self.empty_cells(state):
            if maximising:
                mark = self.symbol
            else:
                mark = self.opponent
            row, col = cell[0], cell[1]
            state[row][col] = mark
            score = self.minimax(state, depth + 1, not maximising)
            state[row][col] = " "
            score[0], score[1] = row, col

            if maximising:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value

        return best

class easy_ai(Agent):    
    
    def move(self, state):
        """
        calls simple move to make a random move
        :param state: the current board
        """
        if self.game_won(state) or self.draw(state):  
            return
        self.simple_move(state, "easy")
        

class medium_ai(Agent):    

    def check_lines(self, grid):   # makes list of all straight lines of grid
        """
        makes the win lines into a list
        :param grid: the board state
        """
        rows = [''.join(grid[i][:]) for i in range(3)]
        columns = [''.join(grid[i][j] for i in range(3)) for j in range(3)]
        diagonals = [''.join(grid[i][i] for i in range(3)), ''.join(grid[i][2 - i] for i in range(3))]
        return rows + columns + diagonals

    def move(self, state):  
        """
        calls check lines to see if it can immidetly win or lose.
        if it can make a medium move, call that function or
        make a random simple move
        :param state: the current board
        """

        if self.game_won(state) or self.draw(state):  
            return

        win_lines = self.check_lines(state)        

        can_win = [line.count(' ') == 1 and line.count(self.symbol) == 2 for line in win_lines]
        can_lose = [line.count(' ') == 1 and line.count(self.opponent) == 2 for line in win_lines]
        if any(can_win):
            self.medium_move(can_win, win_lines, state)
        elif any(can_lose):
            self.medium_move(can_lose, win_lines, state)
        else:
            self.simple_move(state, "medium")  

    def medium_move(self,medium_list,winning_lines , state): 
        """
        converts the position from check lines into board coords.
        :param medium_list: the list of booleans, True is the medium move
        :param winning_lines: the string containing the open cell "X X" or "OO "
        :param state: the board
        """      

        row = medium_list.index(True)
        col = winning_lines[row].index(' ')
        if row < 3:         # Horizontal win 
            new_row = row
            new_col = col
        elif row < 6:       # Vertical win
            new_row = col
            new_col = row -3
        elif row == 6:      # Backslash win
            new_row = col
            new_col = col
        else:               # Slash win
            new_row = col
            new_col = 2 - col
                
        state[new_row][new_col] = self.symbol # place symbol
        print('Making move level "medium"')
        time.sleep(0.5)
        self.grid_draw(state)

class TicTacToe():    

    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']] # This is printed and updated as the game goes on
    
    
    def reset(self):
        """
        When the game is over, reset the board.
        """
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]


    def menu(self):
        """
        Displayed before and after the game.
        the user must inputs the game setup e.g.
        "start user hard"  The user is "X" the ai "O"
        "start easy hard" The easyAI is "X" the hardAI is "O"
        """         

        options = ("user", "easy", "medium", "hard")

        print("\nMAIN MENU\n")
        print("TYPE 'start agent agent' to start a game")
        print(f"agent options are {options}")
        print("e.g. 'start user easy' or 'start medium hard'")
        print("the first agent is 'X' and the second is 'O' ")
        print("\nthe grid is indexed by\n")
        print("1 1 | 1 2| 1 3")
        print("2 1 | 2 2| 2 3")
        print("3 1 | 3 2| 3 3\n")
        while True:
            user_input = input("Enter command: ").split()
            if len(user_input)== 3 and user_input[0] == "start" and user_input[1] in options and user_input[2] in options:
                p1 = self.gen_players(user_input[1], "X", "O") 
                p2 = self.gen_players(user_input[2], "O", "X") 
                self.play(self.board, p1, p2)
            elif user_input[0] == "exit":
                exit()
            else: 
                print("Bad parameters!")

    def gen_players(self, player_in, symbol, opponent):
        """
        after the menu option is selected corresponding
        objects are created and passed to the play
        :param player_in: the type of agent to be created
        :param symbol: The mark that player uses
        :param opponent: the mark their opponent uses 
        """
        if player_in == "user":
            return Human(symbol, opponent)
        elif player_in =="easy":
            return easy_ai(symbol, opponent)
        elif player_in == "medium":
            return medium_ai(symbol, opponent)
        else:
            return hard_AI(symbol, opponent)

    def play(self, state, player1, player2):    
        """
        The game loop. If the game is not over let each player move.
         If its over draw the grid and annouce the winner
         :param player1/2: the object created above
         :param state: the updated game board
        """
        player1.grid_draw(state)
        while not player1.game_won(state) and not player1.draw(state):                            
            player1.move(state)
            
            player2.move(state)
                   

        #player1.grid_draw(state)
        print(player1.who_won(state))
        self.reset()

if __name__ == "__main__":
    game = TicTacToe()
    game.menu()
