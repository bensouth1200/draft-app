import picker
import adp_list

class Cell():
    # class representing a cell on the board

    def __init__(self, draft_rnd, pick, player):

        self.round = draft_rnd
        self.pick = pick
        self.overall_pick = draft_rnd * len(Board.get_pickers()) + pick
        self.player = player

    def set_player(player):

	self.player = player

    def display_cell():

        return self.player



class Board():
    # class representing a draft board

    def __init__(self, rounds, pickers, adp_list, draft_format="standard"):

        self.rounds = rounds 
        self.pickers = pickers
	self.adp_list = adp_list
	self.draft_format = draft_format

        # initialize board here                    
        # nested for loop to create the board.     
        # call cell constructor for each iteration
	self.cells = []
	for i in range(1,rounds+1):
		
		# even rounds traverse pickers backward
		if i % 2 == 0:
			for j in range(len(pickers),0,-1):
				self.cells.append(Cell(i, (len(pickers)+1)-j,pickers[j])) 
		# odd rounds traverse pickers forward
		else: 
			for j in range(1,len(pickers)+1):
				self.cells.append(Cell(i, j, pickers[j]))

    def get_rounds():

        return self.rounds

    def get_pickers():

        return self.pickers

    def set_rounds(rounds):

        self.rounds = rounds

    def set_pickers(pickers):

        self.pickers = pickers

    def get_cell(overall_pick):

        return self.cells[overall_pick].player

    def get_cell(draft_rnd, pick):
        
        return self.cells[draft_rnd * len(pickers) + pick].player

    def set_cell(overall_pick, player):

        self.cells[overall_pick].set_player(player)

    def set_cell(draft_rnd, pick, player):

        self.cells[draft_rnd * len(pickers) + pick].set_player(player)

    def poll_picker(overall_pick, index):
	# what do I do here? save to a cell? just return? 
	self.set_cell(overall_pick, self.get_pickers()[index].think())

    def poll_picker(draft_rnd, pick, index):
	# what do I do here? save to a cell? just return? 
	self.set_cell(draft_rnd, pick, self.get_pickers()[index].think())
    
    def export_table():
	pass

    def update_board():
	pass
