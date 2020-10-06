import ttt_tools as ttt

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
                self.value["f"] = 10
                self.value["s"] = -10
            elif game_result == "s":
                self.value["s"] = 10
                self.value["f"] = -10
            elif game_result == "Draw":
                self.value["f"] = 5
                self.value["s"] = 5
            
            self.is_state_optimal = True
            self.optimal_policy["f"] = -1
            self.optimal_policy["s"] = -1
        
        else:
            self.actions = ttt.find_empty_slots(self.state)


