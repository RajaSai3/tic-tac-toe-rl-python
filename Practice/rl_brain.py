import mdp
import ttt_tools as ttt
import random

#123fssffs

cache = {}

optimal_dict = {}


def list_bool_check(input_list, all_bool = True):

    # if all values of the list are true
    if all_bool:
        return all(input_list)

    # if all values of the list are false
    for value in input_list:
        if value:# if true
            return not value # return false
    return not value # otherwise return true





def return_maximum_value_and_policy(input_dict):

    """
    Receives a dictionary having actions as keys and its action-values as values

    returns the pair of key, value whose value is the maximum

    """

    maximum_value = max(input_dict.values())

    keys_list = []

    for key, value in input_dict.items():

        if value == maximum_value:
            keys_list.append(key)

    if len(keys_list) > 1:
        maximum_action = random.choice(keys_list)

    else:
        maximum_action = keys_list[0]

    return {"action": maximum_action, "value": maximum_value}





def maximum_action_value(state, symbol):

    """
    maximum_action_value(state, symbol)

    Given an input state and a symbol, the function returns the maximum action-value for the state
    by itertating through the state's actions 


    """

    if len(cache[state].actions) == 1:
        action_state = ttt.input_to_board(cache[state].actions[0], state, symbol)
        
        if not action_state in cache:
            cache[action_state] = mdp.MDP(action_state) 
        
        if cache[action_state].is_state_optimal:
            cache[state].optimal_policy["f"] = cache[state].actions[0]
            cache[state].optimal_policy["s"] = cache[state].actions[0]
            cache[state].is_state_optimal = True
        return cache[action_state].value

    elif len(cache[state].actions) > 1:

        f_action_value_dict = {}
        s_action_value_dict = {}

        optimal_list = []
        for action in cache[state].actions:

            action_state = ttt.input_to_board(input_index = action, board_state = state, player_symbol = symbol)

            if not action_state in cache:
                cache[action_state] = mdp.MDP(action_state)

            f_action_value_dict[action] = cache[action_state].value["f"]
            s_action_value_dict[action] = cache[action_state].value["s"]
 
            


            optimal_list.append(cache[action_state].is_state_optimal)


        if list_bool_check(optimal_list):
            cache[state].is_state_optimal = True

            
        final_f = return_maximum_value_and_policy(f_action_value_dict)
        final_s = return_maximum_value_and_policy(s_action_value_dict)

        cache[state].optimal_policy["f"] = final_f["action"]
        cache[state].optimal_policy["s"] = final_s["action"]






        return {"f":final_f["value"], "s":final_s["value"]}







def update_values(state, symbol):

    """
        This function receives the state and the corresponding symbol as inputs and updates the action-values
         until the state's action-value becomes optimal 

         Output: None


    """

    other_symbol = "s" if symbol == "f" else "f" 
    if state in cache:
        if not cache[state].is_state_optimal:

            values_dict = maximum_action_value(state, symbol)
            cache[state].value[symbol] = mdp.rewards["move"] + values_dict[symbol]
            cache[state].value[other_symbol] = values_dict[other_symbol]
        # if cache[state].is_state_optimal:
        #     print(state+" state is optimal")
        # print(state+" is in the cache")
        # pass
    else:
        cache[state] = mdp.MDP(state)
        # print("cached the "+state+" in the 'cache'")
