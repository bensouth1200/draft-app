import board
import picker
import adp_list


def draft(year, draft_format="standard", rounds=15, teams=12, players=''):
	adp_list = ADPList(year, teams, draft_format)

	# need to instantiate pickers here
	
	board = Board(rounds, """ pickers """, adp_list)

	# start game

	# game loop

	# finish game (post-processing?)

###############################################################################
# Things this application needs to do:                                        #
# - Parse argument list to determine settings                                 #
# - Go get ADP List                                                           #
# - Instantiate Board                                                         #
# - Create Players List                                                       #
# - Start Game (GUI? Web App?)                                                #
# - Iterate through the board polling each picker to make_pick()              #
# - Finish Game                                                               #
###############################################################################  
