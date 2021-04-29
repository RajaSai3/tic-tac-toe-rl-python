import json
import ttt_tools as ttt
import train_agent as train
import random

# Run this file to play the game using the stored cache files to test as a sample 

def play_game(content, random_player=False, display_message=True):
    state = "123456789"
    filled_places = []
    if display_message:
        ttt.display_board("123456789")
    for step in range(9):

        if step % 2 == 0:
            if display_message:
                print("Computer's turn: ")
                # print(train.cache[state].actions)
                # print(train.cache[state].values_f)
            index = content[state]
            filled_places.append(index)
            state = ttt.input_to_board(index, state, 'f')
        else:

            if random_player:
                state = train.random_player(state, 's')
            else:
                if display_message:
                    print("Your turn: ")
                while True:
                    index = int(input("Enter index: "))
                    if index in filled_places:
                        print("Choose an empty location in the grid!")
                    else:
                        filled_places.append(index)
                        break
                state = ttt.input_to_board(index, state, 's')

        if display_message:
            translated_state = state.replace("f", "X").replace("s", "O")
            ttt.display_board(translated_state)
        result, info = ttt.check_board_all(state, ['f', 's'])

        if result:
            if info == 'f':
                print("Player X has won the game")
            elif info =='s':
                print("Player s has won the game")
            elif info == "Draw":
                print("Game is a draw")
            break


def second_player_game(content, random_player=False, display_message=True):
    state = "123456789"
    filled_places = []
    if display_message:
        ttt.display_board("123456789")
    for step in range(9):

        if step % 2 == 0: # Human move

            if random_player:
                state = train.random_player(state, 'f')
            else:
                if display_message:
                    print("Your turn: ")
                while True:
                    index = int(input("Enter index: "))
                    if index in filled_places:
                        print("Choose an empty location in the grid!")
                    else:
                        filled_places.append(index)
                        break
                state = ttt.input_to_board(index, state, 'f')

            # --------------------------->


        else: # Agent's (as a secong=d player) move
            index = content[state]
            filled_places.append(index)
            state = ttt.input_to_board(index, state, 's')



        if display_message:
            translated_state = state.replace("f", "X").replace("s", "O")
            ttt.display_board(translated_state)
        result, info = ttt.check_board_all(state, ['f', 's'])

        if result:
            if info == 'f':
                if display_message:
                    print("Player X has won the game")
                # return 'f'
            elif info == 's':
                if display_message:
                    print("Player O has won the game")
                # return 's'
            elif info == "Draw":
                if display_message:
                    print("Game is a draw")
                # return 'd'
            break
            





if __name__ == "__main__":

    while True:
        filename_list = ['min_first_pos1_imp1.json', 'min_first_pos3_imp1.json',
                         'min_first_pos5_imp1.json', 'min_first_pos7_imp1.json',
                         'min_first_pos9_imp1.json', 'min_second.json']
        contents = {}

        filename = random.choice(filename_list)

        with open('json\\min\\'+filename, 'r') as fp:

            contents = json.load(fp)

        if filename == "min_second.json":
            second_player_game(contents)
        else:
            play_game(contents)
        if input("Do you want to play another game: ").lower() == 'n':
            break

