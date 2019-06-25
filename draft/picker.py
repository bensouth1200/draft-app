from numpy import random
from .pickers import fanboy_picker as fanboy
from .pickers import roster_picker as roster
from .pickers import user_picker as user
from .pickers import vb_picker as vb
from .pickers import zeroRB_picker as zeroRB
from .pickers import zeroWR_picker as zeroWR
from .pickers import TE_QB_picker as teqb

class Picker(object):

    def __init__(self, draft_position, rounds, name, fav_team):

        self.picker_type = "picker"
        self.draft_pos = draft_position
        self.players = [-1] * rounds
        self.fav_team = fav_team
	self.name = name

    def pick_team(self, fav_team):
        """ pick a team at random """
        teams = ["none", "PIT", "CIN", "CLE", "BAL", "NYJ", "NE", "BUF", "MIA", "HOU", "JAX", "IND", "TEN", "KC", "LAC", "DEN", "OAK", "SEA", "ARI", "LAR", "SF", "DAL", "PHI", "WAS", "NYG", "CAR", "NO", "TB", "ATL", "MIN", "CHI", "GB", "DET"]
        if fav_team in teams:
            return fav_team
        else:
            return random.choice(teams)

    def factory(picker_type, draft_position, rounds, name, fav_team):
        # this is the facotry to create all the different types of pickers
        if picker_type   == "fanboy": return fanboy.fanboyPicker(draft_position, rounds, name, fav_team)
	elif picker_type == "value-based": return vb.valuePicker(draft_position, rounds, name, fav_team)
        elif picker_type == "zeroRB": return zeroRB.zeroRBPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "zeroWR": return zeroWR.zeroWRPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "user": return user.userPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "roster": return roster.rosterPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "TE/QB": return teqb.TE_QB_Picker(draft_position, rounds, name, fav_team)
        else: return __init__(draft_position, rounds, name, fav_team)
    factory = staticmethod(factory)


    def make_pick(self, player_index, distribution):
        # dumb function. Randomly choose a player from the list       
        # provided based on the percentages provided with the players 
        choice = random.choice(player_index, 1, distribution)
        #print(choice[0]['name'])
        return choice[0]
	

    def think(self, adp_list):
        # here is the function all pickers will override to 
        # fun stuff.                                        
        player_index = adp_list.players[0:5]
        distribution = [0.2, 0.2, 0.2, 0.2, 0.2]
        pick = self.make_pick(player_index, distribution) 
        adp_list.remove_player(pick['name'])
        return pick
