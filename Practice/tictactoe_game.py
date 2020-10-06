import ttt_tools as ttt
import random


initial_state = "123456789"

def bot_engine(state):

    empty_slots = ttt.find_empty_slots(state)
    random_index = random.choice(empty_slots)
    print("Computer's turn ......")
    return random_index

def human_player(state):
    user_input_index = int(input("Input : "))
    print("Human's turn ........")
    return user_input_index

def main_game():
    # x = random.choice([0, 1])
    # bot_engine() if x==0 else human_player()

    first_choice, first_symbol = random.choice([(bot_engine, "X"), (human_player, "O")])

    second_choice, second_symbol = (human_player, "O") if first_choice == bot_engine else (bot_engine, "X")

    current_state = initial_state
    for i in range(9):

        current_player, current_symbol = (first_choice, first_symbol) if i%2 == 0 else (second_choice, second_symbol)
        new_index = current_player(current_state)
        current_state = ttt.input_to_board(new_index, current_state, current_symbol)
        ttt.display_board(current_state)
        result = ttt.check_board(current_state, current_symbol)

        if result == "Draw":
            print("Game is a draw !!!")
            return
        elif result:
            print("{} has won the game".format(current_symbol))
            return current_symbol



counterX = 0
counterO = 0
gameCount = 0



def score_board():
    print("\n---------- Stats -----------")
    print("Total number of games played : {}".format(gameCount))
    print("Number of games computer won : {}".format(counterX))
    print("Number of games you have won : {}".format(counterO))
    print("Winning percentage of Computer : {}".format(round((counterX/gameCount)*100)))
    print("Your winning percentage : {}".format(round((counterO/gameCount)*100)))
    print("-----------------------------\n")

while(True):
    winner = main_game()
    gameCount+=1
    if winner == 'X':
        counterX+=1
    elif winner == 'O':
        counterO+=1
    score_board()
    x = input("Press r to reset scores and n to quit the game:")
    if x == 'r':
        counterX = 0
        counterO = 0
        gameCount = 0
    if x == "n":
        break
