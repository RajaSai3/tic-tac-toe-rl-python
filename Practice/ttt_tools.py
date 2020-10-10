def display_board(board_state):
    if type(board_state) != str:
        raise TypeError('Given board input must be String')

    if len(board_state) != 9:
        raise Exception("Input board string length is not 9")
    
    counter = 0
    print()
    for position in board_state:
        counter+=1
        if counter%3 == 0:
            # paddingString = "\n---------\n" if counter!= 9 else ''
            if counter != 9:
                paddingString = "\n---------\n"
            else:
                paddingString = ''
        else:
            paddingString = " | "


        if position.isnumeric():
            print(" ", end=paddingString)

        else:
            print(position, end=paddingString)

    print("\n\n")


# display_board('OXOXOOOOX')



def input_to_board(input_index, board_state, player_symbol):

    """

    input_to_board(input_index, board_state, player_symbol)

    It returns the a new board state based on the given input index, input board state and player symbol

    Input : input_index where user wants to enter his symbol in the board,
            board_state is the input state of teh board,
            player_symbol is the symbol player wnats to enter in the board (like X/O). 

    Output : returns a new state with the input index


    """

    output_state = ''
    for ind, val in enumerate(board_state):

            if ind == input_index - 1:
                if val.isnumeric():
                    output_state+=player_symbol
                else:
                    raise Exception("Cannot change already assigned board values")
            else:
                output_state+=val

    return output_state


# print(input_to_board(4, "123O5678X", "O"))


def check_board(board_state, player_symbol):
    
    is_board_completely_filled = board_state.isalpha()

    indices_set = set([ind+1 for ind, val in enumerate(board_state) if val == player_symbol])


    if {1, 2, 3}.issubset(indices_set) or {4, 5, 6}.issubset(indices_set) or {7, 8, 9}.issubset(indices_set):

        # print("Row completed..!!!")
        
        # print("Player "+player_symbol+" won the game.")

        return True
    
    if {1, 4, 7}.issubset(indices_set) or {2, 5, 8}.issubset(indices_set) or {3, 6, 9}.issubset(indices_set):

        # print("Column completed..!!!")

        # print("Player "+player_symbol+" won the game.")
        
        return True
    if {1, 5, 9}.issubset(indices_set) or {3, 5, 7}.issubset(indices_set):

        # print("Diagonal completed..!!!")

        # print("Player "+player_symbol+" won the game.")

        return True

    if is_board_completely_filled:
        return "Draw"

    return False





def find_empty_slots(board_state):
    """
    find_empty_slots(board_state)

    It is function that accepts the board state string as input and returns the list of indices from 1 to 9 (not from 0-8).
    These empty slots are places in the board where a user/agent attempt an action.

    Input : 9 - Character board state string
    
    Output : Returns a list of indices where where one can make a new move.

    """
    empty_slot_indices = [ind+1 for ind, val in enumerate(board_state) if val.isnumeric()]

    return empty_slot_indices


# board = "X2XXO6OOX"
# display_board(board)
# print(check_board(board_state=board, player_symbol="O"))
# print(find_empty_slots(board))


def check_board_all(board_state, symbols):

    is_board_completely_filled = board_state.isalpha()

    for player_symbol in symbols:


        indices_set = set([ind+1 for ind, val in enumerate(board_state) if val == player_symbol])

        if {1, 2, 3}.issubset(indices_set) or {4, 5, 6}.issubset(indices_set) or {7, 8, 9}.issubset(indices_set):

            # print("Row completed..!!!")
            # print("Player "+player_symbol+" won the game.")
            return (True, player_symbol)

        if {1, 4, 7}.issubset(indices_set) or {2, 5, 8}.issubset(indices_set) or {3, 6, 9}.issubset(indices_set):

            # print("Column completed..!!!")
            # print("Player "+player_symbol+" won the game.")
            return (True, player_symbol)
        if {1, 5, 9}.issubset(indices_set) or {3, 5, 7}.issubset(indices_set):

            # print("Diagonal completed..!!!")
            # print("Player "+player_symbol+" won the game.")
            return (True, player_symbol)

        if is_board_completely_filled:
            return (True, "Draw")

    return (False, "Game not over")
