import board
import picker
import adp_list

class Config(object):

	def __init__(self):
		#constructor for Config object


pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--year', prompt='What year:', help='What year to simulate a draft of')
@click.option('--draft-format', default='standard', help='What type of scoring will the simulated draft be? (standard, half-ppr, ppr)')
@click.option('--rounds', default=15, help='How many rounds in the draft')
@click.option('--teams', default=12, help='How many teams in the draft')
@click.option('--players', default=[], help='An array of the types of pickers')
@click.option('--position', default=-1, help='Position that you wish to draft from')
@pass_config
def cli(Config):

@cli.command()
@pass_config
def draft(Config)
#def draft(year, draft_format="standard", rounds=15, teams=12, players=[]):
	
	###
	# this could also be moved to the application
	adp_list = ADPList(year, teams, draft_format)
	###

	# need to instantiate pickers here
	if not players:
		return
	
	###
	# should not be done here. We should call the constructors for the
	# pickers in the application itself
	player_vec = []

	for idx, val in enumerate(players):
		player_vec.append(Picker(idx, rounds, ""))
	###

	board = Board(rounds, players, adp_list)

	# game loop
	for i in range(1,rounds+1):

		# even rounds
		if i % 2 == 0:
			for j in range(len(pickers),0,-1):
				board.poll_picker(i, (len(pickers)+1)-j, j)
		# odd rounds		
		else:
			for j in range(1,len(pickers)+1):
				board.poll_picker(i, j, j)

	# finish game (post-processing?)
	return board

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
