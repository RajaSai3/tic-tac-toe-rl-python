import ttt_tools as ttt

rewards = {"win":10, "loss":0, "draw":5, "move":-0.1}

class MDP():
    def __init__(self, state):
        self.state = state
        self.actions = []
        self.values_f = []
        self.values_s = []
        self.is_terminal_state = False
        self.check_terminal_state()
    
    def check_terminal_state(self):

        game_status, game_result = ttt.check_board_all(self.state, ["f", "s"])

        if game_status:

            if game_result == "f":
                self.values_f.append(rewards["win"])
                self.values_s.append(rewards["loss"])
            elif game_result == "s":
                self.values_s.append(rewards["win"])
                self.values_f.append(rewards["loss"])
            elif game_result == "Draw":
                self.values_f.append(rewards["draw"])
                self.values_s.append(rewards["draw"])

            self.is_terminal_state = True

        else:
            self.actions = ttt.find_possible_actions(self.state)
            length_of_actions = len(self.actions)
            self.values_f = [0 for _ in range(length_of_actions)]
            self.values_s = [0 for _ in range(length_of_actions)]

        
