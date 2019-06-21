from numpy import random

class Picker():

    def __init__(self, draft_position, rounds, fav_team):

        self.draft_pos = draft_position
        self.players = [-1] * rounds
	self.fav_team = fav_team

    def pick_team(self, fav_team):
        """ pick a team at random """
	teams = ["none", "PIT", "CIN", "CLE", "BAL", "NYJ", "NE", "BUF", "MIA", "HOU", "JAX", "IND", "TEN", "KC", "LAC", "DEN", "OAK", "SEA", "ARI", "LAR", "SF", "DAL", "PHI", "WAS", "NYG", "CAR", "NO", "TB", "ATL", "MIN", "CHI", "GB", "DET"]
	if fav_team in teams:
		return fav_team
	else:
		return random.choice(teams)

    def make_pick(self, player_index, distribution):
        # dumb function. Randomly choose a player from the list       
        # provided based on the percentages provided with the players 
	choice = random.choice(player_index, 1, distribution)
	print(choice[0]['name'])
	return choice[0]
	

    def think(self, adp_list):
        # here is the function all pickers will override to 
        # fun stuff.                                        
	player_index = adp_list.players[0:5]
	distribution = [0.2, 0.2, 0.2, 0.2, 0.2]
        pick = self.make_pick(player_index, distribution) 
	adp_list.remove_player(pick['name'])
	return pick
