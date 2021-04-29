import json
import mdp
import train_agent as train

def save_cache_to_file(cache_dict, filename, first_player_mode):
    """
        Saves the given cache into a json file on the disk.
    """
    final_dict = {}

    for state in cache_dict:

        if first_player_mode:
            final_dict[state] = {
                "actions": train.cache[state].actions,
                "values_f": train.cache[state].values_f
            }
        else:
            final_dict[state] = {
                "actions": train.cache[state].actions,
                "values_s": train.cache[state].values_s
            }

    with open(filename, 'w') as fj:
        try:

            json.dump(final_dict, fj, indent=4)
            print("Succesfully saved to file", filename)
        except:
            print("Failed to save the file")



def check_all_zeroes(values_list):
    
    for val in values_list:
        if val != 0:
            return False
    return True



def check_terminal_state(values_list):
    if values_list == [mdp.rewards["win"]]:
        return True
    elif values_list == [mdp.rewards["loss"]]:
        return True
    elif values_list == [mdp.rewards["draw"]]:
        return True
    return False


def minify_cache_json_file(filename, first_player_mode):


    """
        Reduce the size of cache json file by replacin the values list with the corresponding 
        optimal action.
    """
    answer_dict = {}
    with open(filename, 'r') as fread:

        read_contents = json.load(fread)

    for state, values in read_contents.items():


        if first_player_mode:
            temp_val = "values_f"
        else:
            temp_val = "values_s"
        if check_terminal_state(values[temp_val]):
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

if __name__ == '__main__':
    filename = input("Provide the file name: ")
    minify_cache_json_file(filename, False)
