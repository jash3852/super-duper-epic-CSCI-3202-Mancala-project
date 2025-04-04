import random

class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        """
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones 
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player-1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]
        self.p2_mancala_index = len(self.board)-1
        self.p1_turn_counter = 0
        self.p2_turn_counter = 0
        
        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('P1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            else:    
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            
        print('         {}         '.format(player_1_mancala))
        turn = 'P1' if self.current_player == 1 else 'P2'
        print('Turn: ' + turn)
        
    def valid_move(self, pit_index):
        """
        Function to check if the pit chosen by the current_player is a valid move.
        """

        pit_has_stones = self.board[pit_index] > 0
        
        player_pits = self.get_player_pits()
        indexOfFirstPit = player_pits[0]
        indexOfLastPit = player_pits[1]
        pit_on_current_player_side = indexOfFirstPit <= pit_index <= indexOfLastPit

        pit_is_not_mancala = (pit_index != self.p1_mancala_index) and (pit_index != self.p2_mancala_index)

        return pit_has_stones and pit_on_current_player_side and pit_is_not_mancala

    def random_move_generator(self):
        """
        Function to generate random valid moves with non-empty pits for the random player
        """
        
        possible_moves = self.get_valid_moves()
        return random.choice(possible_moves)
    
    def play(self, pit):
        """
        This function simulates a single move made by a specific player using their selected pit. It primarily performs three tasks:
        1. It checks if the chosen pit is a valid move for the current player. If not, it prints "INVALID MOVE" and takes no action.
        2. It verifies if the game board has already reached a winning state. If so, it prints "GAME OVER" and takes no further action.
        3. After passing the above two checks, it proceeds to distribute the stones according to the specified Mancala rules.

        Finally, the function then switches the current player, allowing the other player to take their turn.
        """

        # print("Player", self.current_player, "chose pit:", pit)
        pit_index = self.get_pit_index(pit)

        if (self.valid_move(pit_index)):
            if (self.winning_eval()):
                self.clean_stones()
                # print("GAME OVER")
            else:
                self.moves.append((self.current_player, pit))
                self.distribute_stones(pit_index)
                self.switch_player()

            if self.current_player == 1:
                self.p1_turn_counter += 1
            else:
                self.p2_turn_counter += 1
        else:
            print("INVALID MOVE")
        
        return self.board
    
    def winning_eval(self):
        """
        Function to verify if the game board has reached the winning state.
        Hint: If either of the players' pits are all empty, then it is considered a winning state.
        """
        
        no_stones_in_player_1_pits = all([self.board[pit] == 0 for pit in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1)])
        no_stones_in_player_2_pits = all([self.board[pit] == 0 for pit in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1)])

        return no_stones_in_player_1_pits or no_stones_in_player_2_pits



    #
    # Lots of helper functions
    #

    def get_player_pits(self):
        """
        Return the repective pit indices list for `current_player` with respect to the `board` list.

        Parameters:
            None

        Returns:
            List of int - List of pit indices for `current_player` with respect to the `board` list
        """
        
        return self.p1_pits_index if self.current_player == 1 else self.p2_pits_index

    def get_pit_index(self, pit):
        """
        Returns the index of `pit` with respect to the `board` list

        Parameters:
            pit (int) - A value betwen 1 and `pits_per_player` inclusive

        Returns:
            int - A value between 0 and len(board) inclusive which represents an index in `board`
        """
        
        startOfPlayer2Pits = self.p2_pits_index[0]

        match (self.current_player):
            case 1:
                return pit - 1
            case 2:
                return pit + startOfPlayer2Pits - 1
        
    def in_opponent_mancala(self, pit_index):
        """
        Check if the current `pit_index` represents the opponent's mancala pit.

        Parameters:
            pit_index (int) - A value between 0 and len(board) inclusive which represents the index of a pit on `current_player`'s side

        Returns:
            Boolean - True if `pit_index` is the opponent's mancala pit and False otherwise.
        """
        
        return (self.current_player == 1 and pit_index == self.p2_mancala_index) or (self.current_player == 2 and pit_index == self.p1_mancala_index)

    def distribute_stones(self, pit_index):
        """
        Takes stones from `pit_index` on board and distributes them throughout the board in accordance to the Mancala rules.

        Parameters:
            pit_index (int) - A value between 0 and len(board) inclusive which represents the index of a pit on `current_player`'s side

        Returns:
            None
        """
        
        current_stones = self.board[pit_index]
        self.board[pit_index] = 0

        while current_stones > 0:
            pit_index = (pit_index + 1) % len(self.board)

            if self.in_opponent_mancala(pit_index):
                continue

            self.board[pit_index] += 1
            current_stones -= 1

        if self.valid_move(pit_index) and self.board[pit_index] == 1:
            # Last stone placed in `pit_index` on `current_player`'s side
            opposite_pit_index = self.get_opposite_pit_index(pit_index)
            current_player_mancala_index = self.get_player_mancala_index()

            self.board[current_player_mancala_index] += self.board[pit_index] + self.board[opposite_pit_index]
            self.board[pit_index] = 0
            self.board[opposite_pit_index] = 0

    def switch_player(self):
        """
        Switches `current_player` between 1 and 2

        Parameters:
            None

        Returns:
            None
        """
    
        offset = 1

        self.current_player = self.current_player % 2 + offset

    def get_pit_from_index(self, pit_index):
        """
        Returns the pit value of `pit_index` with respect to the `board` list and `current_player`

        Parameters:
            pit_index (int) - A value between 0 and len(board) inclusive which represents an index in `board`

        Returns:
            int - A value betwen 1 and `pits_per_player` inclusive
        """

        startOfPlayer2Pits = self.p2_pits_index[0]
        
        match(self.current_player):
            case 1:
                return pit_index + 1
            case 2:
                return pit_index - startOfPlayer2Pits + 1
            
    def get_opposite_pit_index(self, pit_index):
        """
        Return the pit index of the pit opposite to `pit_index`

        Parameters:
            pit_index (int) - A value between 0 and len(board) inclusive which represents an index in `board`

        Returns:
            int - A value between 0 and len(board) inclusive which represents an index in `board` representing the opposite pit
        """

        pit = self.get_pit_from_index(pit_index)
        self.switch_player()
        opposite_pit = self.pits_per_player - pit + 1
        opposite_pit_index = self.get_pit_index(opposite_pit)
        self.switch_player()

        return opposite_pit_index
    
    def get_player_mancala_index(self):
        """
        Returns the index in `board` that corresponds to `current_player`'s mancala pit

        Parameters:
            None

        Returns:
            int - Index of `current_player`'s mancala in the board
        """

        match(self.current_player):
            case 1:
                return self.p1_mancala_index
            case 2:
                return self.p2_mancala_index
            
    def clean_stones(self):
        """
        Move remaining stones to the respective player's Mancalla following the end of the game.

        Parameters:
            None

        Returns:
            None
        """

        if all([self.board[pit] == 0 for pit in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1)]):
            # Player 1 has no stones left
            for pit_index in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1):
                self.board[self.p2_mancala_index] += self.board[pit_index]
                self.board[pit_index] = 0
        else:
            # Player 2 has no stones left
            for pit_index in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1):
                self.board[self.p1_mancala_index] += self.board[pit_index]
                self.board[pit_index] = 0

    def get_valid_moves(self):
        """
        Returns a list of pit values (between 1 and `pits_per_player` inclusive) that can be played on `current_player`'s turn

        Parameters:
            None

        Returns:
            List of int - Pit values (between 1 and `pits_per_player` inclusive) that can be played on `current_player`'s turn
        """

        player_pits = self.get_player_pits()
        return [self.get_pit_from_index(pit_index) for pit_index in range(player_pits[0], player_pits[1] + 1) if self.valid_move(pit_index)]