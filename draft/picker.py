from numpy import random

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
        if picker_type   == "fanboy": return fanboyPicker(draft_position, rounds, name, fav_team)
	elif picker_type == "value-based": return valuePicker(draft_position, rounds, name, fav_team)
        elif picker_type == "zeroRB": return zeroRBPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "zeroWR": return zeroWRPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "user": return userPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "roster": return rosterPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "TE/QB": return TE_QB_Picker(draft_position, rounds, name, fav_team)
        else: return __init__(draft_position, rounds, name, fav_team)
    factory = staticmethod(factory)

    def assign_pickers(number):
        pickers = ["fanboy", "value-based", "zeroRB", "zeroWR", "roster", "TE/QB"]
        pick = []
        for x in range(number):
            pick.append(random.choice(pickers)) 
    
        return pick
    assign_pickers = staticmethod(assign_pickers)

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

###############################################################
# class to simulate a fanboy drafter. Players on the picker's #
# favorite team will be overvalued                            #
###############################################################
class fanboyPicker(Picker):

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(fanboyPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "fanboy"

    def think(self, adp_list):
        super(fanboyPicker, self).think(adp_list)



###############################################################
# class to simulate a value-based draft strategy              #
###############################################################
class valuePicker(Picker):

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(valuePicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "value-based"

    def think(self, adp_list):
        super(valuePicker, self).think(adp_list)



###############################################################
# class to simulate a drafter using the zero RB strategy      #
###############################################################
class zeroRBPicker(Picker):

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(zeroRBPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "zero RB"

    def think(self, adp_list):
        super(zeroRBPicker, self).think(adp_list)




##############################################################
# class to simulate a drafter using the zero WR strategy     #
##############################################################
class zeroWRPicker(Picker):


    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(zeroWRPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "zero WR"

    def think(self, adp_list):
        super(zeroWRPicker, self).think(adp_list)



##################################################################
# class to simulate a drafter that prioritizes QBs and TEs       #
##################################################################
class TE_QB_Picker(Picker):


    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(TE_QB_Picker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "TE/QB"

    def think(self, adp_list):
        super(TE_QB_Picker, self).think(adp_list)



############################################################
# class to let user pick in draft                          #
############################################################
class userPicker(Picker):


    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(userPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "user"

    def think(self, adp_list):
        super(userPicker, self).think(adp_list)



#########################################################################
# class to simulate a roster-based approach to drafting.                #
# this drafter will prioritize filling open roster spots to bench spots #
#########################################################################
class rosterPicker(Picker):


    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(rosterPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "roster"

    def think(self, adp_list):
        super(rosterPicker, self).think(adp_list)

