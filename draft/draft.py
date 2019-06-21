from board import Board
from picker import Picker
from adp_list import ADPList
import click

class Config(object):

	def __init__(self):
		#constructor for Config object
		self.year = -1
		self.draft_format = ""
		self.rounds = -1
		self.teams = -1
		self.players = []
		self.position = -1
		self.adp_list = []


draft_settings = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--year', default=2016, help='What year to simulate a draft of.')
@click.option('--draft_format', default='standard', help='What type of scoring will the simulated draft be? (standard, half-ppr, ppr)')
@click.option('--rounds', default=14, help='How many rounds in the draft.')
@click.option('--teams', default=12, help='How many teams in the draft.')
@click.option('--players', default=["test1", "test2"], help='An array of the types of pickers.')
@click.option('--position', default=-1, help='Position that you wish to draft from.')
@draft_settings
def draft(Config, year, draft_format, rounds, teams, players, position):
	
	"""
	This application will simulate a fantasy draft and export the draft board(s) in a JSON file format. 
	"""
	adp_list = ADPList(year, teams, draft_format)

	if not players:
		return
	
	players = ["picker","picker","picker","picker","picker","picker","picker","picker","picker","picker","picker","picker"]
	player_vec = []

	for idx, val in enumerate(players):
		player_vec.append(Picker(idx, rounds, ""))
	###
	#print("player_vec: %s" % player_vec)
	
	Config.year = year
	Config.draft_format = draft_format
	Config.rounds = rounds
	Config.teams = teams
	Config.pickers = player_vec
	Config.position = position
	Config.adp_list = adp_list

@draft.command()
@draft_settings
def single(Config):

	""" This command will simulate a single draft. """
	board = Board(Config.rounds, Config.pickers, Config.adp_list)

	print("Starting Draft")
	# game loop
	for i in range(1,Config.rounds+1):

		# even rounds
		if i % 2 == 0:
			for j in range(len(Config.pickers)-1,0,-1):
				print("picking round %s, " % str(i), "pick %s" % str((len(Config.pickers)+1)-j))
				board.poll_picker(i, (len(Config.pickers)+1)-j, (len(Config.pickers)+1)-j-1)
		# odd rounds		
		else:
			for j in range(1,len(Config.pickers)+1):
				print("picking round %s, " % str(i), "pick %s" % str(j))
				board.poll_picker(i, j, j-1)

	# finish game (post-processing?)
	print(type(board))
	return board

@draft.command()
@click.option('--randomize', is_flag=True)
@click.argument('drafts')
@draft_settings
def repeated(Config, drafts):
	""" This will run the specific configuration of a draft multiple times.\n
	ARGUMENTS:\n
	drafts INTEGER - number of times to simulate the draft """
	pass

@draft.command()
@click.argument('team1')
@click.argument('team2')
@click.argument('team3')
@draft_settings
def triangle(Config, team1, team2, team3):
	""" This will take in three type of pickers and create a triangular matrix with every configuration of these three pickers in the draft.  \n
	ARGUMENTS:\n
	team1 STRING - first type of picker\n
	team2 STRING - second type of picker\n
	team3 STRING - third type of picker\n
	"""
	pass

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
