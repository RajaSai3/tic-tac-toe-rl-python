# old_q_value = 0
# count=0

alpha = 0.7
gamma = 0.99

# q = 0
# reward = -0.25
# maxq = 10

# while True:
    
#     old_q_value = q
#     q = round((1-alpha)*q + alpha*(reward+(gamma*maxq)-q),4)

#     count+=1

#     print("-------------------------")
#     print("Iteration", count)
#     print("Q value is:",q)
#     print("Old Q value is:", old_q_value)

#     if (count%100 == 0):
#         print(count,"Number of iterations completed")
#         print("Q value is:",q)
#         print("Old Q value is:", old_q_value)
        
#     if q == old_q_value:
#         break

# print("Number of iterations:",count)
# print("Value",q)
import mdp

def action_diff(state1, state2):
    for i in range(9):
        if state1[i]!=state2[i]:
            if state1[i].isnumeric():
                return int(state1[i])
            else:
                return int(state2[i])


def print_diagnostics():

    for state, mdp_obj in cache.items():
        print("-----------", state, "-------------------")
        print("Actions  ----> ", mdp_obj.actions)
        print("Values_f  ----> ", mdp_obj.values_f)
        print("Values_s  ----> ", mdp_obj.values_s)
        print("Terminal State  ----> ", mdp_obj.is_terminal_state)
        print("---------------------------------------")

cache = {}

states = ['123456789', 'f23456789', 'f234s6789', 'f234s678f',
          'fs34s678f', 'fs34s67ff', 'fs34s6sff', 'fsf4s6sff', 
          'fsfss6sff', 'fsfssfsff']

def load_states():
    for state in states:
        if state not in cache:
            cache[state] = mdp.MDP(state)


def forward_learning(count):
    print("Learning forward")

    print("\nAfter", count, "iterations\n")
    for _ in range(count):        
        for index, state in enumerate(states):
            if cache[state].is_terminal_state:
                continue

            action = action_diff(states[index],states[index+1] )
            action_index = cache[state].actions.index(action)

            if index%2 == 0:
                # First player value modifications 

                if index == len(states)-2:
                    temp_index = index+1
                else:
                    temp_index = index+2
                cache[state].values_f[action_index] = round((1 - alpha)*(cache[state].values_f[action_index]) + alpha*(-0.1+ gamma*
                max(cache[states[temp_index]].values_f)), 5)
            else:
                # Second player value modification


                cache[state].values_s[action_index] = round((1 - alpha)*(cache[state].values_s[action_index]) + alpha*(-0.1+ gamma*
                min(cache[states[index+2]].values_s)), 5)


def reverse_learning(count):
    print("Learning in reverse")

    print("\nAfter", count, "iterations\n")
    for _ in range(count): 
        reversed_states = list(reversed(states))
        for index, state in enumerate(reversed_states):
            if cache[state].is_terminal_state:
                continue

            action = action_diff(reversed_states[index], reversed_states[index-1])
            action_index = cache[state].actions.index(action)

            if index%2 == 1:
                # First player value modifications 
                if index == 1:
                    temp_index = index-1
                else:
                    temp_index = index-2
                cache[state].values_f[action_index] = round((1 - alpha)*(cache[state].values_f[action_index]) + alpha*(-0.1+ gamma*
                max(cache[reversed_states[temp_index]].values_f)), 5)
            else:
                # Second player value modification
                cache[state].values_s[action_index] = round((1 - alpha)*(cache[state].values_s[action_index]) + alpha*(-0.1+ gamma*
                min(cache[reversed_states[index-2]].values_s)), 5)
 
if __name__ == "__main__":

    
    load_states()
    if input("Enter f or r: ") == 'f':
        forward_learning(15)
    else:
        reverse_learning(15)
    # print("\nAfter",count,"iterations\n")
    print_diagnostics()
