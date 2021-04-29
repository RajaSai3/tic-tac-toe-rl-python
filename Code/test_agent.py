import train_agent as train
import ttt_tools as ttt
from cache_manipulation import save_cache_to_file

# This is the target file

losses_list = []
loss_actions = []




def first_player_game(random_player = False, display_message=True):

    """
        Allows the agent to make first move in the game by returning action values from the cache.
        The second player can be a human or automated  depending on the requirement.
    """
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


def second_player_game(random_player=False, display_message=True):
       
    """
        Allows the agent to make second move in the game by returning action values from the cache.
        The first player can be a human or automated  depending on the requirement.
    """
    state = "123456789"
    loss_actions.clear()
    if display_message:
        ttt.display_board("123456789")
    for step in range(9):

        if step % 2 == 1:
            if display_message:
                print("Computer's turn: ")
                print(train.cache[state].actions)
                print(train.cache[state].values_s)
            index = train.exploit(state, 's')
            loss_actions.append(index)
            state = ttt.input_to_board(index, state, 's')
        else:

            if random_player:
                index = train.random_player(state, 'f', return_state=False)
                loss_actions.append(index)
                state = ttt.input_to_board(index, state, 'f')
            else:
                if display_message:
                    print("Your turn: ")
                    
                while True:
                    index = int(input("Enter index: "))
                    loss_actions.append(index)
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
            if info == 'f':
                losses_list.append(tuple(loss_actions))
            return info

def compute_stats(f_lose, s_lose, draw, game_count, first_player_mode):
    
    """
        Used to print the given values in a legible format
    """


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


    """
        Allows the human to test the trained agent by providing input through the keyboard.
    """
    f_lose = 0
    s_lose = 0
    draw = 0
    num_of_game = 0

    while True:
        if first_player_mode:
            answer = first_player_game()
        else:
            answer = second_player_game()
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
                save_cache_to_file(train.cache, filename, first_player_mode)
            break
    compute_stats(f_lose, s_lose, draw, num_of_game, first_player_mode)


def automatic_test_game(num_of_games, first_player_mode = True, display_statistics = True):
    """
        Used to test the trained agent automatically by the system itself without the
        intervention of human. 
    """
    if display_statistics:
        if first_player_mode:
            print(f"\n Automated accuracy check in {num_of_games} for first player \n")
        else:
            print(f"\n Automated accuracy check in {num_of_games} for second player \n")
    f_lose = 0
    s_lose = 0
    draw = 0

    for _ in range(num_of_games):
        if first_player_mode:
            answer = first_player_game(random_player=True, display_message = False)
        else:
            answer = second_player_game(random_player=True, display_message=False)

        if answer == 'f':
            s_lose += 1
        elif answer == 's':
            f_lose += 1
        elif answer == "Draw":
            draw += 1

    if display_statistics:
        compute_stats(f_lose, s_lose, draw, num_of_games, first_player_mode)

    if first_player_mode:
        return f_lose
    else:
        return s_lose



def final_game(num_of_iter, rate, first_player_mode, analysis_mode=False):

    """
        Used for training the agent either as first player or second player depending on the 
        value of parameter 'first_player_mode' .
    
    """

    print("Please wait, the AI is training")
    
    if first_player_mode:
        train.train_first_player(num_of_iter, rate)
    else:
        train.train_second_player(num_of_iter, rate)
        train_agent_from_losses_second_player()
    
    losses = automatic_test_game(100000,first_player_mode)


    if losses/10000 < 0.1 and not analysis_mode:
        if input("Do you want to play the game: ").lower() == 'y':
            human_test_game(first_player_mode)
        else:
            message = input("Do you want to save this into a json file? < yes | no >: ").lower()
            if  message == 'yes' or message == 'y':
                filename = input("Enter the file name: ")
                save_cache_to_file(train.cache, filename, first_player_mode)

    return losses
                


def test_both_players(iterations = 1000000, rate = 0.015, discount = 0.99, is_loss_computed=True):


    """
        Used to test agent playing as both the first and second player at the same time
    """
    train.train_both_players(iterations, rate, discount)
    # train_agent_from_losses_second_player()
    if is_loss_computed:
        first_loss = automatic_test_game(100000, first_player_mode=True)
        print(f"Loss when the agent is first player: {first_loss} ")
        second_loss = automatic_test_game(100000, first_player_mode=False)
        print(f"Loss when the agent is first player: {second_loss} ")




def train_agent_from_losses_second_player():

    """
        Train the agent (second player) from its losses.
    """
    count = 0
    while True:
        count+=1
        automatic_test_game(100000, False)
        losses_set = set(losses_list)
        print(f"Length of losses list is {len(losses_set)}")
        print(losses_set)
    
        if len(losses_set) == 0:
            if input("Do you want to save this as a file: ").lower() == 'y':
                file = input("Enter the file name to save the second player cache: ")
                save_cache_to_file(train.cache, file, False)
            print(count)
            print("Done")
            break
            # return count
            
            
        train.train_from_losses(losses_set, rate, discount)
        losses_list.clear()

if __name__ == '__main__':
        iters = 1000000
        rate = 0.015
        discount = 0.99
        is_first_player_mode = False


        final_game(iters, rate, first_player_mode=is_first_player_mode, analysis_mode=True)
        
    
