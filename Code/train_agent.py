import ttt_tools as ttt
import random
import mdp
import tqdm

cache = {}



def random_player(state, player_symbol, return_state = True):
    # if state not in cache:
    #     cache[state] = mdp.MDP(state)
    index =  random.choice(cache[state].actions)
    state = ttt.input_to_board(index, state, player_symbol)
    if return_state:
        return state
    else:
        return index

def human_player(state, player_symbol):
    while True:
        index = int(input("Enter the index to place your symbol: "))
        if not index in cache[state].actions or index == '\n':
            print("Choose an empty location in the grid!")
        else:
            state = ttt.input_to_board(index, state, player_symbol)
            return state



explore = random_player


def exploit(state, player_symbol):

    if state not in cache:
        cache[state] = mdp.MDP(state)

    if player_symbol == 'f':
        max_value = max(cache[state].values_f)
        max_val_index = cache[state].values_f.index(max_value)
        return cache[state].actions[max_val_index]

    elif player_symbol == 's':
        max_value = max(cache[state].values_s)
        max_val_index = cache[state].values_s.index(max_value)
        return cache[state].actions[max_val_index]
    



def train_player_per_episode(states_list, symbol, learning_rate, discount_factor):

    """
    This function accepts a list of states played in a tic-tac-toe game in sequence, reverses the list,
    and updates the q-values of each state-action pair.

    """

    # learning_rate = 0.01
    # discount_factor = 0.99

    if cache[states_list[-1]].is_terminal_state:
        states_list.reverse()

    for index, state in enumerate(states_list):
        # if state not in cache:
        #     cache[state] = mdp.MDP(state)
        if cache[state].is_terminal_state:
            continue

        action_number = ttt.action_diff(states_list[index], states_list[index-1], symbol)
        action_index = cache[state].actions.index(action_number)

        if symbol == 'f':
            cache[state].values_f[action_index] = (1 - learning_rate)*cache[state].values_f[action_index] + learning_rate*(mdp.rewards["move"] + discount_factor*max(cache[states_list[index-1]].values_f))
            cache[state].values_f[action_index] = round(cache[state].values_f[action_index], 4)
        elif symbol == 's':
            cache[state].values_s[action_index] = (1 - learning_rate)*cache[state].values_s[action_index] + learning_rate*(mdp.rewards["move"] + discount_factor*max(cache[states_list[index-1]].values_s))
            cache[state].values_s[action_index] = round(cache[state].values_s[action_index], 4)


def train_first_player(num_of_iterations, rate=0.01, discount_factor = 0.99):

    """
    This function plays a tic-tac-toe game involving two random players.
    All the states produces withhin the game are stored in a list and is forwarded to training_player_per_each_episode 
    function for actual training.

    """

    print("\nTraining first player, please wait .... \n")
    for _ in tqdm.trange(num_of_iterations):

        state = "123456789"
        states_list = []
        for step in range(10):

            if state not in cache:
                cache[state] = mdp.MDP(state)

            if cache[state].is_terminal_state:
                states_list.append(state)
                break

            if step%2 == 0:
                # First Player Move
                states_list.append(state)

                # Start Exploration - Exploitation trade off here ---------
                state = explore(state, 'f')
                # ---------------------------------------------------------
                
            else:
                # Random player move
                state = random_player(state, 's')

        train_player_per_episode(states_list, symbol = 'f', learning_rate = rate, discount_factor = discount_factor)


def train_second_player(num_of_iterations, rate):
    print("\nTraining second player, please wait .... \n")
    

    for _ in tqdm.trange(num_of_iterations):

        # v = random.random()
        # if v < 0.5:
        #     state = "1234f6789"
        # else:
        #     state = "123456789"
        state = "123456789"
        states_list = []
        for step in range(10):

            if state not in cache:
                cache[state] = mdp.MDP(state)

            if cache[state].is_terminal_state:
                states_list.append(state)
                break

            if step % 2 == 0:   # First Player Move, Random player move
                state = random_player(state, 'f')
                # if state not in cache:
                #     cache[state] = mdp.MDP(state)

            else:   # Second player move
                states_list.append(state)

                # Start Exploration - Exploitation trade off here ---------
                state = explore(state, 's')
                # v = 1
                # if (random.random()<=v):
                #     # v = v - 0.0001
                # else:
                #     index = exploit(state, 's')
                #     state = ttt.input_to_board(index, state, 's')
                # ---------------------------------------------------------


                # if state not in cache:
                #     cache[state] = mdp.MDP(state)

        for _ in range(1):
            train_player_per_episode(states_list, symbol = 's', learning_rate=rate, discount_factor=0.99)




def train_both_players(iterations, rate, discount = 0.99):

    print("Training for both the players ............")


    for _ in tqdm.trange(iterations):

        state = "123456789"
        first_states_list = []
        second_states_list = []

        for step in range(10):

            if state not in cache:
                cache[state] = mdp.MDP(state)
            
            if cache[state].is_terminal_state:
                first_states_list.append(state)
                second_states_list.append(state)
                break

            if step%2 == 0: # First player move
                first_states_list.append(state)
                state = explore(state, 'f')
            else:
                second_states_list.append(state)
                state = explore(state, 's')

        train_player_per_episode(first_states_list, 'f', rate, discount)
        train_player_per_episode(second_states_list, 's', rate, discount)




def train_from_losses(losses_set: set, rate, discount): # Only for second player


    for indices_tuple in losses_set:

        states_list = []
        state = "123456789"
        # ttt.display_board(state)
        for index, action in enumerate(indices_tuple):

            
            if index % 2 == 0:
                symbol = "X" 
                # state = ttt.input_to_board(action, state, symbol)
            else:
                symbol = "O"
                states_list.append(state.replace("X", "f").replace("O", "s"))
            
            state = ttt.input_to_board(action, state, symbol)
            if index == len(indices_tuple)-1 and state not in states_list:
                states_list.append(state.replace("X", "f").replace("O", "s"))

        train_player_per_episode(states_list, "s", rate, discount)
        

            # ttt.display_board(state)



