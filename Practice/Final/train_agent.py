import ttt_tools as ttt
import random
import mdp
import tqdm

cache = {}

def action_diff(state1, state2, player_symbol):
    for i in range(9):
        if (state1[i] != state2[i]) and ((state1[i] == player_symbol) or (state2[i] == player_symbol)):
            if state1[i].isnumeric():
                return int(state1[i])
            else:
                return int(state2[i])

def random_player(state, player_symbol):
    index =  random.choice(cache[state].actions)
    state = ttt.input_to_board(index, state, player_symbol)
    return state

def human_player(state, player_symbol):
    index = int(input("Enter the index to place your symbol: "))
    state = ttt.input_to_board(index, state, player_symbol)
    return state

# def explore(state):
#     index = random.choice(cache[state].actions)
#     return index

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

    # learning_rate = 0.01
    # discount_factor = 0.99

    if cache[states_list[-1]].is_terminal_state:
        states_list.reverse()

    for index, state in enumerate(states_list):
        # if state not in cache:
        #     cache[state] = mdp.MDP(state)
        if cache[state].is_terminal_state:
            continue

        action_number = action_diff(states_list[index], states_list[index-1], symbol)
        action_index = cache[state].actions.index(action_number)

        if symbol == 'f':
            cache[state].values_f[action_index] = (1 - learning_rate)*cache[state].values_f[action_index] + learning_rate*(mdp.rewards["move"] + discount_factor*max(cache[states_list[index-1]].values_f))
        elif symbol == 's':
            cache[state].values_s[action_index] = (1 - learning_rate)*cache[state].values_s[action_index] + learning_rate*(mdp.rewards["move"] + discount_factor*max(cache[states_list[index-1]].values_s))



def train_first_player(num_of_iterations, rate=0.01):

    print("\nTraining first player, please wait .... \n")
    for _ in tqdm.trange(num_of_iterations):

        state = "123456789"
        states_list = []
        for step in range(9):

            if state not in cache:
                cache[state] = mdp.MDP(state)

            if step%2 == 0:
                # First Player Move
                states_list.append(state)

                # Start Exploration - Exploitation trade off here ---------
                state = explore(state, 'f')
                # ---------------------------------------------------------
                
                if state not in cache:
                    cache[state] = mdp.MDP(state)

            else:
                # Random player move
                state = random_player(state, 's')
                if state not in cache:
                    cache[state] = mdp.MDP(state)

            if cache[state].is_terminal_state:
                states_list.append(state)
                break
        train_player_per_episode(states_list, symbol = 'f', learning_rate = rate, discount_factor = 0.99)


def train_second_player(num_of_iterations, rate):
    print("\nTraining second player, please wait .... \n")

    for _ in tqdm.trange(num_of_iterations):

        v = random.random()
        if v < 0.5:
            state = "1234f6789"
        else:
            state = "123456789"
        states_list = []
        for step in range(9):

            if state not in cache:
                cache[state] = mdp.MDP(state)

            if step % 2 == 0:
                # First Player Move
                # Random player move
                state = random_player(state, 'f')
                if state not in cache:
                    cache[state] = mdp.MDP(state)

            else:
                # Second player move
                states_list.append(state)

                # Start Exploration - Exploitation trade off here ---------
                state = explore(state, 's')
                # ---------------------------------------------------------


                if state not in cache:
                    cache[state] = mdp.MDP(state)

            if cache[state].is_terminal_state:
                states_list.append(state)
                break
        train_player_per_episode(states_list, symbol = 's', learning_rate=rate, discount_factor=0.99)





