import ttt_tools as ttt

rewards = {"win": 10, "loss": -10, "draw": 5, "move": -1}

class MDP():
    def __init__(self, state):
        self.state = state
        self.actions = []
        self.is_state_optimal = False
        self.value = {"f": 0, "s": 0}
        self.optimal_policy = {"f":0, "s": 0}
        self.is_terminal_state()

    def is_terminal_state(self):

        game_status, game_result = ttt.check_board_all(self.state, ["f", "s"])

        if game_status:
            
            if game_result == "f":
                self.value["f"] = rewards["win"]
                self.value["s"] = rewards["loss"]
            elif game_result == "s":
                self.value["s"] = rewards["win"]
                self.value["f"] = rewards["loss"]
            elif game_result == "Draw":
                self.value["f"] = rewards["draw"]
                self.value["s"] = rewards["draw"]
            
            self.is_state_optimal = True
            self.optimal_policy["f"] = -1
            self.optimal_policy["s"] = -1
        
        else:
            self.actions = ttt.find_empty_slots(self.state)


