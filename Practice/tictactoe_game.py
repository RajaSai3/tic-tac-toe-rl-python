import ttt_tools as ttt
import random
import random_game_generator as rgg
import rl_brain as rl

initial_state = "123456789"


def find_next_symbol(state):
    """
    Receives the state as input and returns the next symbol that must be
    applied on the state

    """

    if state.count("f") == state.count("s"):
        return "f"
    return "s"


def random_bot(state):
    # print("Computer's turn ......")
    empty_slots = ttt.find_empty_slots(state)
    random_index = random.choice(empty_slots)
    return random_index

def bot_engine(state):

    # print("Computer's turn ........")

    symbol = find_next_symbol(state)

    return rl.cache[state].optimal_policy[symbol]


def human_player(state):
    print("Human's turn ........")
    user_input_index = int(input("Input : "))
    return user_input_index


def select_first_player_randomly(players_dict):
    """
    Selects who would play the first move of the game randomly from both the players

    The function expects to receive a dictionary with only two key-value pairs as there cannot be more than two players in tic-tac-toe 

    input : A dictionary with symbols as keys and its corresponding players (function references) as values

    output :  A dictionary with randomly generated first and second players with their symbols

    """
    if len(players_dict) != 2:
        raise Exception("Game should have only two players !")

    keys = list(players_dict.keys())

    first_symbol = random.choice(keys)

    first_player = players_dict[first_symbol]
    keys.remove(first_symbol)

    second_symbol = keys[0]

    second_player = players_dict[second_symbol]

    result_dict = {"first": {"symbol": first_symbol, "player": first_player}, "second": {
        "symbol": second_symbol, "player": second_player}}
    return result_dict



def main_game():
    temp_dict = select_first_player_randomly(
        {"X": bot_engine, "O": human_player})

    first_player = temp_dict["first"]["player"]
    first_symbol = temp_dict["first"]["symbol"]

    second_player = temp_dict["second"]["player"]
    second_symbol = temp_dict["second"]["symbol"]

    current_state = initial_state
    for i in range(1, 10):

        current_player, current_symbol = (first_player, first_symbol) if i%2 == 1 else (second_player, second_symbol)
        
        translated_current_state = current_state.replace(first_symbol, "f").replace(second_symbol, "s")
        
        new_index = current_player(translated_current_state)
        current_state = ttt.input_to_board(new_index, current_state, current_symbol)

        ttt.display_board(current_state)
        result = ttt.check_board(current_state, current_symbol)

        if result == "Draw":
            print("Game is a draw !!!")
            return "Draw"
        elif result:
            if current_symbol == "X":
                print("Computer has won the game")
            elif current_symbol == "O":
                print("You have won the game")
            return current_symbol







def score_board(counterX, counterO, counter_draw, gameCount):
    print("\n---------- Stats -----------")
    print("Total number of games played : {}".format(gameCount))
    print("Number of games computer won : {}".format(counterX))
    print("Number of games you have won : {}".format(counterO))
    print("Winning percentage of Computer : {}".format(round((counterX/gameCount)*100)))
    print("Your winning percentage : {}".format(round((counterO/gameCount)*100)))
    print("-----------------------------\n")



print("Please wait, the computer is getting ready....")
rgg.connect(30000)
print("Done .... ")

counterX = 0
counterO = 0
counter_draw = 0
gameCount = 0

iterations = 10000
temp = 1

while(True):
    winner = main_game()
    gameCount+=1
    if winner == 'X':
        counterX+=1
    elif winner == 'O':
        counterO+=1
    elif winner == "Draw":
        counter_draw+=1

    score_board(counterX, counterO, counter_draw, gameCount)
    x = input("Press r to reset scores and n to quit the game:")
    if x == 'r':
        counterX = 0
        counterO = 0
        counter_draw = 0
        gameCount = 0
    if x == "n":
        break




# score_board(counterX, counterO, counter_draw, gameCount)
