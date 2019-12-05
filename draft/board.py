import draft.picker as picker
import draft.adp_list as adp_list
import scipy.stats as ss

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
    		#print("round ", str(i), ": ", range(len(pickers),0,-1))
                for j in range(len(pickers),0,-1):
		    #print("creating Cell round %s, " % str(i), "pick %s, " % str((len(pickers)+1)-j), "picker %s" % j)
                    self.cells.append(dict(draft_rnd=i,pick=(len(pickers)+1)-j,picker=pickers[j-1],player="none")) 
	    # odd rounds traverse pickers forward
            else: 
		#print("round ", str(i), ": ", range(1,len(pickers)+1))
                for j in range(1,len(pickers)+1):
		    #print("creating Cell round %s, " % str(i), "pick %s, " % str(j), "picker %s" % j)
                    self.cells.append(dict(draft_rnd=i, pick=j, picker=pickers[j-1], player="none"))

    def get_rounds(self):

        return self.rounds

    def get_pickers(self):

        return self.pickers

    def set_rounds(self, rounds):

        self.rounds = rounds

    def set_pickers(self, pickers):

        self.pickers = pickers

    def get_cell(self, overall_pick):

        return self.cells[overall_pick].player

    def get_cell(self, draft_rnd, pick):
        
        return self.cells[draft_rnd * len(pickers) + pick].player

    #def set_cell(self, overall_pick, player):

    #    self.cells[overall_pick].set_player(player)

    def set_cell(self, draft_rnd, pick, player):

        self.cells[(draft_rnd-1) * len(self.pickers) + pick-1]["player"] = player
	#print("cell index: %s, " % ((draft_rnd-1) * len(self.pickers) + pick), "round: %s, " % draft_rnd, "pick: %s" % pick)

    #def poll_picker(overall_pick, index):
	# what do I do here? save to a cell? just return? 
	#self.set_cell(overall_pick, self.get_pickers()[index].think())

    def poll_picker(self, draft_rnd, pick, index):
	# what do I do here? save to a cell? just return? 
        self.set_cell(draft_rnd, pick, self.get_pickers()[index].think(self.adp_list))
    
    def export_table(self):
        pass

    def update_board(self):
        pass

    def calculate_rank():
        points = []
        for i in len(self.pickers):
            points.append(self.pickers[i].season_points)
        
        return ss.rankpick(points, method='min')

