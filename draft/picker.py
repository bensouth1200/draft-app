from numpy import random

class Picker(object):

    def __init__(self, draft_position, rounds, name, fav_team):

        self.picker_type = "picker"
        self.draft_pos = draft_position
        self.players = []
	self.name = name
        self.fav_team = self.pick_team(fav_team)
        self.lineup = dict(QB=1, RB=2, WR=2, TE=1, FLEX=1, DEF=1, PK=1, BNCH=rounds-9)

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
        #print(choice[0]['name'])
	if self.lineup[choice[0]['position']] == 0:
            if self.lineup['FLEX'] == 0:
                self.lineup['BNCH'] = self.lineup['BNCH'] - 1
            else:
                self.lineup['FLEX'] = self.lineup['FLEX'] - 1
        else:
            self.lineup[choice[0]['position']] = self.lineup[choice[0]['position']] - 1
        return choice[0]
	

    def think(self, adp_list):
        # here is the function all pickers will override to 
        # fun stuff.                                        
        player_index = adp_list.players[0:5]
        distribution = [0.2, 0.2, 0.2, 0.2, 0.2]
        pick = self.make_pick(player_index, distribution) 
        adp_list.remove_player(pick['name'])
        self.players.append(pick)
        return pick

###############################################################
# class to simulate a fanboy drafter. Players on the picker's #
# favorite team will be overvalued                            #
###############################################################
class fanboyPicker(Picker):

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(fanboyPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "fanboy"
        #print("fanboy team: %s" % self.fav_team)

    def think(self, adp_list):
        team_players = []
        for x in adp_list.players:
            if x['team'] == self.fav_team:
                team_players.append(x)

        if len(adp_list.players) >= 5:
            player_index = adp_list.players[0:4]
            if not team_players:
                player_index.append(adp_list.players[4])
            else:
                player_index.append(team_players[0])
        #print(player_index)
            distribution = [0.225,0.225,0.225,0.225,0.1]
        else:
            player_index = adp_list.players
            distribution = [1.0/len(adp_list.players) for x in range(len(adp_list.players))]

        pick = super(fanboyPicker, self).make_pick(player_index, distribution)
        print(pick['name'])
        adp_list.remove_player(pick['name'])
        self.players.append(pick)
        return pick
        #super(fanboyPicker, self).think(adp_list)



###############################################################
# class to simulate a value-based draft strategy              #
###############################################################
class valuePicker(Picker):

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(valuePicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "value-based"

    def think(self, adp_list):
        return super(valuePicker, self).think(adp_list)



###############################################################
# class to simulate a drafter using the zero RB strategy      #
###############################################################
class zeroRBPicker(Picker):

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(zeroRBPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "zero RB"

    def think(self, adp_list):
        # split the adp list into RBs and everyone else
        rbs  = []
        qbs  = []
        wrs  = []
        tes  = []
        defk = []
        for x in adp_list.players:
            if x['position'] == 'RB':
                rbs.append(x)
            elif x['position'] == 'WR':
                wrs.append(x)
            elif x['position'] == 'QB':
                qbs.append(x)
            elif x['position'] == 'TE':
                tes.append(x)
            else:
                defk.append(x)

        if len(self.players) < 5:
            player_index = wrs[0:3]
            player_index.append(qbs[0])
            player_index.append(tes[0])
            distribution = [0.25,0.25,0.25,0.125,0.125]
        elif len(self.players) < 12:
            player_index = rbs[0:3]
            player_index.append(wrs[0])
            player_index.append(qbs[0])
            player_index.append(tes[0])
            distribution = [0.3,0.3,0.3,0.033,0.034,0.033]
        elif len(self.players) < 12:
            # conditional here to pick up what we dont have?
            player_index = wrs[0:2]
            if qbs:
                player_index.append(qbs[0])
            if rbs:
                player_index.append(rbs[0])
            if tes:
                player_index.append(tes[0])
            distribution = [1.0/len(player_index) for x in range(len(player_index))]
        else:
            player_index = defk
            if qbs:
                player_index.append(qbs[0])
            if rbs:
                player_index.append(rbs[0])
            if tes:
                player_index.append(tes[0])
            distribution = [1.0/len(player_index) for x in range(len(player_index))]
            
	pick = super(zeroRBPicker, self).make_pick(player_index, distribution)
        adp_list.remove_player(pick['name'])
        self.players.append(pick)
        return pick




##############################################################
# class to simulate a drafter using the zero WR strategy     #
##############################################################
class zeroWRPicker(Picker):


    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(zeroWRPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "zero WR"

    def think(self, adp_list):
        # split the adp list into RBs and everyone else
        rbs  = []
        qbs  = []
        wrs  = []
        tes  = []
        defk = []
        for x in adp_list.players:
            if x['position'] == 'RB':
                rbs.append(x)
            elif x['position'] == 'WR':
                wrs.append(x)
            elif x['position'] == 'QB':
                qbs.append(x)
            elif x['position'] == 'TE':
                tes.append(x)
            else:
                defk.append(x)

        if len(self.players) < 5:
            player_index = rbs[0:3]
            player_index.append(qbs[0])
            player_index.append(tes[0])
            distribution = [0.25,0.25,0.25,0.125,0.125]
        elif len(self.players) < 8:
            player_index = wrs[0:3]
            player_index.append(rbs[0])
            player_index.append(qbs[0])
            player_index.append(tes[0])
            distribution = [0.3,0.3,0.3,0.033,0.034,0.033]
        elif len(self.players) < 12:
            # conditional here to pick up what we dont have?
            player_index = wrs[0:2]
            if qbs:
                player_index.append(qbs[0])
            if rbs:
                player_index.append(rbs[0])
            if tes:
                player_index.append(tes[0])
            distribution = [1.0/len(player_index) for x in range(len(player_index))]
        else:
            player_index = defk
            if qbs:
                player_index.append(qbs[0])
            if rbs:
                player_index.append(wrs[0])
            if tes:
                player_index.append(tes[0])
            distribution = [1.0/len(player_index) for x in range(len(player_index))]
            
	pick = super(zeroWRPicker, self).make_pick(player_index, distribution)
        adp_list.remove_player(pick['name'])
        self.players.append(pick)
        return pick



##################################################################
# class to simulate a drafter that prioritizes QBs and TEs       #
##################################################################
class TE_QB_Picker(Picker):


    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(TE_QB_Picker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "TE/QB"

    def think(self, adp_list):
        return super(TE_QB_Picker, self).think(adp_list)



############################################################
# class to let user pick in draft                          #
############################################################
class userPicker(Picker):


    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(userPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "user"

    def think(self, adp_list):
        return super(userPicker, self).think(adp_list)



#########################################################################
# class to simulate a roster-based approach to drafting.                #
# this drafter will prioritize filling open roster spots to bench spots #
#########################################################################
class rosterPicker(Picker):


    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(rosterPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "roster"

    def think(self, adp_list):
        return super(rosterPicker, self).think(adp_list)

