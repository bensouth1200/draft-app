import player
import picker
import adp_list

class Cell():
    # class representing a cell on the board

    def __init__(self, draft_rnd, pick, player):

        self.round = draft_rnd
        self.pick = pick
        self.overall_pick = draft_rnd * len(Board.get_pickers()) + pick
        self.player = player

    def display_cell():

        return self.player



class Board():
    # class representing a draft board

    def __init__(self, rounds, pickers, adp_list):

        self.rounds = rounds
        self.pickers = pickers
	self.adp_list = adp_list

        # initialize board here                    
        # nested for loop to create the board.     
        # call cell constructor for each iteration 

    def update_board():


    def get_rounds():

        return self.rounds

    def get_pickers():

        return self.pickers

    def set_rounds(rounds):

        self.rounds = rounds

    def set_pickers(pickers):

        self.pickers = pickers

    def get_cell(overall_pick):

    def get_cell(draft_rnd, pick):

    def set_cell(overall_pick, player):

    def set_cell(draft_rnd, pick, player):

    def export_table():

