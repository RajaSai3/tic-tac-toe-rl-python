import train_agent as train
import ttt_tools as ttt
import json

# This is the target file

def save_to_file(cache_dict, filename):
    final_dict = {}

    for state, value in cache_dict.items():

            final_dict[state] = {
                "actions": train.cache[state].actions,
                "values_f": train.cache[state].values_f,
                "values_s": train.cache[state].values_s
            }

    with open(filename, 'w') as fj:
        try:
            # fj.write(json.dumps(final_dict, indent=2))
            json.dump(final_dict, fj, indent=4)
            print("Succesfully saved to file", filename)
        except:
            print("Failed to save the file")

def play_game(random_player = False, display_message=True):
    state = "123456789"
    if display_message:
        ttt.display_board("123456789")
    for step in range(9):

        if step%2 ==0:
            if display_message:
                print("Computer's turn: ")
                print(train.cache[state].actions)
                print(train.cache[state].values_f)
            index = train.exploit(state, 'f')
            state = ttt.input_to_board(index, state, 'f')
        else:

            if random_player:
                state = train.random_player(state, 's')
            else:
                if display_message:
                    print("Your turn: ")
                while True:
                    index = int(input("Enter index: "))
                    if not index in train.cache[state].actions or index == '\n':
                        print("Choose an empty location in the grid!")
                    else:
                        break
                state = ttt.input_to_board(index, state, 's')

        if display_message:
            translated_state = state.replace("f", "X").replace("s", "O")
            ttt.display_board(translated_state)
        result, info = ttt.check_board_all(state, ['f', 's'], display_message)

        if result:
            return info


def second_play_game(random_player=False, display_message=True):
    state = "123456789"
    if display_message:
        ttt.display_board("123456789")
    for step in range(9):

        if step % 2 == 1:
            if display_message:
                print("Computer's turn: ")
                print(train.cache[state].actions)
                print(train.cache[state].values_s)
            index = train.exploit(state, 's')
            state = ttt.input_to_board(index, state, 's')
        else:

            if random_player:
                state = train.random_player(state, 'f')
            else:
                if display_message:
                    print("Your turn: ")
                    
                while True:
                    index = int(input("Enter index: "))
                    if not index in train.cache[state].actions or index == '\n':
                        print("Choose an empty location in the grid!")
                    else:
                        break

                state = ttt.input_to_board(index, state, 'f')

        if display_message:
            translated_state = state.replace("f", "X").replace("s", "O")
            ttt.display_board(translated_state)
        result, info = ttt.check_board_all(state, ['f', 's'], display_message)

        if result:
            return info

def compute_stats(f_lose, s_lose, draw, game_count, first_player_mode):
    
    print(" ----- Statistics Report ----- ")
    print("Number of games played", game_count)
    if first_player_mode:
        print("Games AI has lost", f_lose)
        print("Games opponent has lost", s_lose)
    else:
        print("Games AI has lost", s_lose)
        print("Games opponent has lost", f_lose)
    print("Games drawn", draw)
    print("-------------------------------")



def human_test_game(first_player_mode=True):

    f_lose = 0
    s_lose = 0
    draw = 0
    num_of_game = 0

    while True:
        if first_player_mode:
            answer = play_game()
        else:
            answer = second_play_game()
        num_of_game+=1

        if answer == 'f':
            s_lose+=1
        elif answer == 's':
            f_lose+=1
        elif answer == "Draw":
            draw+=1
        
        message = input("Do you want to play another game? < yes | no >: ").lower()
        if  message == 'no' or message == 'n':
            message = input("Do you want to save this into a json file? < yes | no >: ").lower()
            if  message == 'yes' or message == 'y':
                filename = input("Enter the file name: ")
                save_to_file(train.cache, filename)
            break
    compute_stats(f_lose, s_lose, draw, num_of_game, first_player_mode)


def automatic_test_game(num_of_games, first_player_mode = True, factor=1):
    print("\n Automated accuracy check\n")
    f_lose = 0
    s_lose = 0
    draw = 0

    for _ in range(num_of_games):
        if first_player_mode:
            answer = play_game(random_player=True, display_message = False)
        else:
            answer = second_play_game(random_player=True, display_message=False)

        if answer == 'f':
            s_lose += 1
        elif answer == 's':
            f_lose += 1
        elif answer == "Draw":
            draw += 1

    if num_of_games%factor == 0:
        compute_stats(f_lose, s_lose, draw, num_of_games, first_player_mode)

    if first_player_mode:
        return f_lose
    else:
        return s_lose

def final_game(num_of_iter, rate, first_player_mode):
    # rate = 0.0005
    # temp = 5000000
    # first_player_mode = False


    print("Please wait, the AI is training")
    # train_player(temp, rate)
    if first_player_mode:
        train.train_first_player(num_of_iter, rate)
    else:
        train.train_second_player(num_of_iter, rate)
    # print("Training done")
    losses = automatic_test_game(10000,first_player_mode)
    # print("Losses", losses)
    if losses < 10:
        human_test_game(first_player_mode)
    # return losses


final_game(num_of_iter = 5000000, rate = 0.0005, first_player_mode = True)