from board import Board
from adp_list import ADPList
from numpy import random
import picker
import click
import json

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
@click.option('--players', default=[], help='An array of the types of pickers.')
@click.option('--position', default=-1, help='Position that you wish to draft from.')
@draft_settings
def draft(Config, year, draft_format, rounds, teams, players, position):
        
        """
        This application will simulate a fantasy draft and export the draft board(s) in a JSON file format. 
        """
        adp_list = ADPList(year, teams, draft_format)

        #players = ["fanboy","fanboy","fanboy","fanboy","fanboy","fanboy","fanboy","fanboy","fanboy","fanboy","fanboy","fanboy"]
        if not players:
            players = picker.Picker.assign_pickers(teams)

	names = pick_team_names(teams)
        picker_vec = []

        for idx, val in enumerate(players):
                picker_vec.append(picker.Picker.factory(players[idx], idx, rounds, names[idx], ''))
		print(picker_vec[idx].picker_type)
        ###
        #print("player_vec: %s" % player_vec)
        
        Config.year = year
        Config.draft_format = draft_format
        Config.rounds = rounds
        Config.teams = teams
        Config.pickers = picker_vec
        Config.picker_types = players
        Config.position = position
        Config.adp_list = adp_list
	Config.team_names = names

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
                        for j in range(len(Config.pickers),0,-1):
                                print("picking round %s, " % str(i), "pick %s" % str((len(Config.pickers)+1)-j))
                                #board.poll_picker(i, (len(Config.pickers)+1)-j, (len(Config.pickers)+1)-j-1)
                                board.poll_picker(i, (len(Config.pickers)+1)-j, j-1)
                # odd rounds            
                else:
                        for j in range(1,len(Config.pickers)+1):
                                print("picking round %s, " % str(i), "pick %s" % str(j))
                                #board.poll_picker(i, j, j-1)
                                board.poll_picker(i, j, j-1)

        # finish game (post-processing?)
        for x in board.cells:  
                x["picker"] = x["picker"].picker_type

        # create a json object of the board to export
        meta = dict(year=Config.year,rounds=Config.rounds,pickers=Config.picker_types,draft_format=Config.draft_format,team_names=Config.team_names)
        json_board = json.dumps(dict(board=board.cells,meta=meta)) 

	with open("test.json", "w") as write_file:
		json.dump(json_board,write_file)
        return json_board

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

def determine_picker_type(picker_type, draft_position, rounds, name, fav_team=''):
	pickers = {
		"roster": "rosterPicker",
		"fanboy": "fanboyPicker",
		"zeroRB": "zeroRBPicker",
		"zeroWR": "zeroWRPicker",
		"vb": "valuePicker",
		"user": "userPicker",
		"teqb": "TE_QB_Picker"
	}
	print(picker_type)
	constructor = getattr(picker_type, pickers.get(picker_type, "Picker"))
	print(constructor)
	return constructor(draft_position, rounds, name, fav_team)
		

def pick_team_names(number):
 
	team_names = ["Hot Chubb Time Machine", "Josh Jacobs Jingleheimer Schmidt", "Baby Got Dak", "Murray Up and Wait", "Deshaun of the Dead", "Happy Golladays", "Country Road, Take Mahomes", "Jason Kelce's Tailor", "All Barkley, All Bite", "Baker's Dozen", "The Fabulous Baker Boy", "Guns & Rosen", "A Kiss from a Rosen", "Rosen Up You Bow", "Golden Tate Warriors", "Watson In Your Wallet", "View From Lamar", "Dak to the Future", "Golden Taint", "Lights, Kamara, Action", "Kamara Shy", "Shake it Goff", "Turn Your Head and Goff", "Hartline Bling", "All I Do is Winston", "Zeke Squad", "Saving Matt Ryan", "PokeMoncrief", "Little Red Fournette", "Fournettecation", "Unsolicited Dak Pics", "Lamar, Mr. Jackson if You're Nasty", "Hide & Zeke", "Dalvin & the Chipmunks", "When the Le'Veon Breaks", "Le'Veon la vida Loca", "Le'Veon a Prayer", "Yippee Ki Yay Justin Tucker", "Highway to Bell", "Game of Jones", "Julio Think You Are?", "Julio Let the Dogs Out", "Goff Balls", "My Ball Zach Ertz", "My TE Ertz When Eifert", "Eiferted", "It's Too Late to Say Amari", "Amari 2600", "Have Amari Christmas", "Stairway to Evans", "Knockin on Evans Door", "Hot Lockett", "Roethlisberger Helper", "Gurley Things", "2 Gurley's 1 Cup", "Runs Like a Gurley", "The Gurley Gates", "A Zeke Outlook", "All About That Bosa", "Mr. Rodgers' Neighborhood", "From Wentz You Came", "Wents, Twice -- Three Times a Lady", "Dude, Where's Derek Carr?", "Forte inch Ditka", "Steady Cams", "Inglorious Bradfords", "Breaking Bradford", "Chronic Masterdeflater", "Check My Balls", "Discount Belichek", "Yo Belicheck Yo Self", "Mariota Had a Little Lamb", "Super Mario-ta", "Marcus Mari...otto", "Turn Down for Watt", "JJ S.W.A.T.T. Team", "1.21 JJ WATTS", "The JPP Fireworks Incident", "You Down With JPP?", "Hernandez Hit Men", "Wham! Bam! Thank you Cam!", "You Kaeperncik the Future", "Geno 911!", "Show Me Your TDs", "Multiple Goregasms", "13 Reasons Ajayi", "InstaJimmyGraham", "Ladies and Edelman", "Backfields and McCoys", "Inglorious Staffords", "Stafford Infection", "Mike Vick in a Box", "Montee Can Buy You Happiness", "My Percy's on Broadway", "In a Van Down by the Rivers", "Cry Me a Rivers", "Pitch a Trent", "50 Trent", "Drake's New Favorite Team", "Waka Flacco Flame", "U Mad Bro?", "Abdullah Oblongata", "Rudolph Redzone Reindeer", "Trolling Crabtree", "Kung Suh Panda", "Suh Girls, One Cup", "Boy Named Suh", "No Money Manziel", "Evil Empire", "Revis' Vineyard", "Bend it Like Beckham Jr.", "O-Dell No", "OBJYN", "Jay-Z's My Agent", "To Khalil a Mockingbird", "The Sony Side of Life", "Off the Tennessee the Whiz", "Remember the Titans", "Kissing Suzy Kolber", "Smokin' Jay Cutler", "Teenage Mutant Ninja Bortles", "Poppin' Bortles", "Diry Sanchez Butt-Fumblers", "Kaepernick Swag", "Mannings' O-Face", "Sherman's Last Rant", "The Boldin the Beautiful", "Gisele's Bundchens", "Mr. UGG Boots", "Here's My Number, So Call Me Brady", "Brady Gaga", "The Brady Bunch", "Luck Beat a Brady Tonight", "Call Me the Brees", "Hooked on a Thielen", "No Romo", "80% Mental, 40% Physical", "Laces Out", "Show Me the Money", "Big Ol' Bortles", "Not Racist Redskins", "Hard Knocks Life", "Forgetting Brandon Marshall", "It's Always Runny in Phiiladelphia", "Favre Dollar Footlong", "Crab-leg Bootleg", "Luckness Monster", "Up All Night to Get Luck-y", "Red Hot Julius Peppers", "Slow White Bronco", "Mixon, Mix-off", "Green Eggs and Cam", "O.J.'s Parole Board", "Baby Got Dak", "Dak and Yellow", "Nuthin' But a Jimmy G Thang", "Truth or Derrius", "Instant Kamara", "Pimpin' Ain't Breesy", "Kerryon My Warward Son", "Mariota Had a Little Lamb", "Rolls Royces", "MegaErtz", "I Gotta Thielen", "Male Pattern Baldwiness", "Bad JuJu", "JuJu Know What I'm Sayin'?", "Can You Diggs It?", "Diggs in a Blanket", "The Mixon Administration", "Mixon Match", "Gore Values", "Suh-and-aHalf Men", "Suh-Tang Clan", "Peachy Keenum", "Rage Against the Vereen", "Kissing Cousins Good-bye", "Too Good to be Trubisky", "Thor: Ragnow-Rock", "Hot Lockett", "Ingram Toenails", "Clam Crowder", "T.Y. Very Much", "T.Y. Dolla $ign", "Tate Misbehavin'", "I'll Make You Jameis", "All You Snead is Love", "Bortles Service", "Feel the Hurns", "Hyde and Go Luck Yourself", "Eastbound and Brown", "Lamar the Merrier!", "Serial Miller", "Lamar You Serious?", "We're Allen this Together", "It's Von Like Donkey Kong", "Rebel Yeldon's", "Take Goff the Lights", "Don't Eli To My Face", "Let Sleeping Dogs Eli", "More than a Thielen", "Sony Side Up", "A Rosen By Any Other Name...", "Mayfield of Dreams", "Three Blind Guice", "Shake-N-Bakers", "AP's Daycare", "Half-Baked", "Zeke and Destroy"]
	
	return [random.choice(team_names) for x in range(number)]
