import ttt_tools as ttt
import random
import rl_brain as rl
import sys
import time
import mdp

initial_state = "123456789"
# rl.update_values(initial_state, "f")


def find_next_symbol(state):
    """
    Receives the state as input and returns the next symbol that must be
    applied on the state

    """


    if state.count("f") == state.count("s"):
        return "f"
    return "s"

def translate_state(state, symbol_dict):

    temp_state = state
    for key, val in symbol_dict.items():
        temp_state = temp_state.replace(key, val)
    return temp_state

def bot_engine(state):

    # rl.update_values(state)

    empty_slots = ttt.find_empty_slots(state)
    random_index = random.choice(empty_slots)
    # print("Computer 1 turn ......")
    return random_index


def human_player(state):
    user_input_index = int(input("Input : "))
    print("Human's turn ........")
    return user_input_index

def bot_engine2(state):

    # rl.update_values(state)

    empty_slots = ttt.find_empty_slots(state)
    random_index = random.choice(empty_slots)
    # print("Computer 2 turn ......")
    return random_index

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

    result_dict = {"first": {"symbol":first_symbol, "player":first_player}, "second": {"symbol":second_symbol, "player":second_player}}
    return result_dict




def main_game():
    temp_dict = select_first_player_randomly({"X": bot_engine, "O": bot_engine2})

    first_player = temp_dict["first"]["player"]
    first_symbol = temp_dict["first"]["symbol"]

    second_player = temp_dict["second"]["player"]
    second_symbol = temp_dict["second"]["symbol"]

    symbol_map = {first_symbol: "f", second_symbol: "s"}
    current_state = initial_state
    for i in range(1, 10):

        current_player, current_symbol = (first_player, first_symbol) if i % 2 == 1 else (second_player, second_symbol)

        translated_current_state = translate_state(current_state, symbol_map)
        if not translated_current_state in rl.cache:
            if current_state == "123fssffs":
                print("Let's debug")
            rl.cache[translated_current_state] = mdp.MDP(translated_current_state)
        rl.update_values(translated_current_state, symbol_map[current_symbol])

        new_index = current_player(current_state)
        current_state = ttt.input_to_board( new_index, current_state, current_symbol)
        # ttt.display_board(current_state)
        result = ttt.check_board(current_state, current_symbol)




        if result == "Draw":

            # print("Game is a draw !!!")
            
            return "Draw"
        elif result:

            # print("{} has won the game".format(current_symbol))

            return current_symbol




def score_board(counterX, counterO, counter_draw, gameCount):
    print("\n---------- Stats -----------")
    print("Total number of games played : {}".format(gameCount))
    print("Number of games computer won : {}".format(counterX))
    print("Number of games you have won : {}".format(counterO))
    print("Number of games that have been drawn : {}".format(counter_draw))
    print("Winning percentage of Computer : {} %".format(
        round((counterX/gameCount)*100, 2)))
    print("Your winning percentage : {} %".format(
        round((counterO/gameCount)*100, 2)))
    print("-----------------------------\n")


def optimality_stats(cache, report=False):
    length_of_cache = 0
    count_of_optimal_states = 0
    for key in cache:
        if cache[key].is_state_optimal:
            count_of_optimal_states += 1
        length_of_cache += 1

    percentage = round(count_of_optimal_states * 100/length_of_cache, 2)

    if report:
        print("\n----------------Final report ----------------\n")
        print("Number of iterations: {}".format(maximum_iterations))
        print("Number of optimal states: {}".format(count_of_optimal_states))
        print("number of elements in cache: {}".format(length_of_cache))
        print("Optimality percentage: {} %".format(percentage))
        print("Length of cache is {}".format(len(cache)))
        print("Size of cache is {} MB".format(
            round((cache.__sizeof__())/1000000, 2)))
        print("\n---------------------------------------------\n")

    return percentage

def boost_optimality(cache, iterations):

    while iterations > 0:
        # keys =list(cache.keys()).copy()
        # keys.reverse()
        for key in cache.keys():
            rl.update_values(key, find_next_symbol(key))
        iterations-=1
    print("Finished optimization")


def test_game(iterations):

    """
    
    Used for testing purpose

    """

    board1 = [initial_state, "123X56789", "123XO6789", "12XXO6789", "O2XXO6789", "O2XXOX789", "O2XXOX78O"]
    # board2 = [initial_state, "12345678X", "1234O678X", "X234O678X", "X234O6O8X", "X234O6OXX", "X2O4O6OXX"]


    for i in range(iterations):
        print("Iteration {}....".format(i+1))
        count = 1
        for state in board1:
            translated_state = state.replace("X", "f").replace("O", "s")
            # loop_symbol = "f" if (index+1)%2 == 1 else "s"
            rl.update_values(translated_state, find_next_symbol(translated_state))
            count+=1
        

def connect(maximum_iterations):
    counterX = 0
    counterO = 0
    counter_draw = 0
    gameCount = 0
    iterator = 0
    while(iterator < maximum_iterations):
        winner = main_game()
        gameCount += 1
        iterator+=1
        if winner == 'X':
            counterX += 1
        elif winner == 'O':
            counterO += 1
        elif winner == "Draw":
            counter_draw+=1
        if iterator%10000 == 0:
            score_board(counterX, counterO, counter_draw, gameCount)


        # x = input("Press r to reset scores and n to quit the game:")
        # if x == 'r':
        #     counterX = 0
        #     counterO = 0
        #     gameCount = 0
        # if x == "n":
        #     break


a = time.time()
print("Started the loop ... ")

maximum_iterations = 50000

# connect(maximum_iterations)
print("Before starting the game: {} and its length: {}".format(rl.cache, len(rl.cache)))

connect(maximum_iterations)

b = time.time()

optimality_stats(rl.cache, report = True)

boost_optimality(rl.cache, 100)
print("Time taken {} seconds".format(round(b-a, 2)))

optimality_stats(rl.cache, report=True)
print("Debug statement")

