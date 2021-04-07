import json
import mdp

def check_all_zeroes(values_list):
    
    for val in values_list:
        if val != 0:
            return False
    return True


# def check_terminal_state(state):

#       game_status, game_result = ttt.check_board_all(state, ["f", "s"])

#        if game_status:

#             if game_result == "f":
#                 values_f.append(rewards["win"])
#                 values_s.append(rewards["loss"])
#             elif game_result == "s":
#                 values_s.append(rewards["win"])
#                 values_f.append(rewards["loss"])
#             elif game_result == "Draw":
#                 values_f.append(rewards["draw"])
#                 values_s.append(rewards["draw"])

#             is_terminal_state = True

#         else:
#             actions = ttt.find_possible_actions(state)
#             length_of_actions = len(actions)
#             values_f = [0 for _ in range(length_of_actions)]
#             values_s = [0 for _ in range(length_of_actions)]

def cts(values_list):
    if values_list == [mdp.rewards["win"]]:
        return True
    elif values_list == [mdp.rewards["loss"]]:
        return True
    elif values_list == [mdp.rewards["draw"]]:
        return True
    return False


def simplify_json(filename, first_player_mode):
    answer_dict = {}
    with open(filename, 'r') as fread:

        read_contents = json.load(fread)

    for state, values in read_contents.items():


        if first_player_mode:
            temp_val = "values_f"
        else:
            temp_val = "values_s"
        if cts(values[temp_val]):
            continue
    
        if check_all_zeroes(values[temp_val]):
            continue
        
        maximum_value = max(values[temp_val])
        maximum_value_index = values[temp_val].index(maximum_value)
        
        optimal_action = values["actions"][maximum_value_index]

        answer_dict[state] = optimal_action

    with open("min_"+filename, 'w') as fwrite:
        json.dump(answer_dict, fwrite)
        print("Successfully minimized the data into a  new file min_"+filename)
        

    # print(answer_dict)

filename = input("Provide the file name: ")
simplify_json(filename, True)
