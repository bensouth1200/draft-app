from numpy import random
import pandas as pd
import numpy as np
import scipy.stats as ss
from sklearn.preprocessing import OneHotEncoder
from keras.models import Sequential
from keras.models import Model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import BatchNormalization
from keras.layers import Conv1D
from keras.layers import AveragePooling1D
from keras.layers import MaxPooling1D
from keras.layers import Flatten
from keras.layers import Input
from keras.layers import concatenate
from keras.layers import Embedding
from keras.utils import plot_model
from keras.models import load_model
#import models

# this function will read in player data from the ADP List and 
# do some preprocessing to get it ready to pass to the CNN
def pre_process_player_data(full_adp_list):
    # convert the adp_list from a list of dicts to a pandas dataframe
    #print(full_adp_list)
    all_players = pd.DataFrame(full_adp_list,columns=['name','adp','times_drafted','team','high','low','adp_formatted','player_id','position','bye','stdev'])

    encoded_cols = ['name','team','position']
    encoder = OneHotEncoder(handle_unknown='ignore')
    encoded_data = encoder.fit_transform(all_players[encoded_cols]).toarray()
    encoded_data = pd.DataFrame(encoded_data,columns=encoder.get_feature_names(['name','team','position']))

    return pd.concat([all_players['adp'],all_players['bye'],encoded_data],axis=1,sort=False)

    
# this function will read in the current state of the draft and encode 
# is into an input vector for the MLP
def pre_process_state_data(team_roster, available_players, full_adp_list):
    
    roster = []
    available = []
    
    for x in full_adp_list:
        if x in team_roster:
            roster.append([1])
        else:
            roster.append([0])

        if x in available_players:
            available.append([1])
        else:
            available.append([0])

    return np.concatenate((roster,available))


    # fit a OneHotEncoder to the player names
    #one_hot = OneHotEncoder(handle_unknown='ignore')
    #player_names = [x['name'] for x in full_adp_list]
    #one_hot.fit([player_names])

    # grab just the names of the players in both roster and available players
    #team_names = [x['name'] for x in team_roster]
    #available_names = [x['name'] for x in available_players]
    #print("TEAM NAMES = %s" % team_names)
    #print("AVAILABLE_NAMES = %s" % available_names)
    # now create one hot encoded array for the roster
    #roster = np.zeros(len(full_adp_list))
    #for x in [team_names]:
    #    roster = np.logical_or(roster,one_hot.transform([x]).toarray())

    # create one hot encoded array for the available players
    #available = np.zeros(len(full_adp_list))
    #for x in available_names:
    #    available = np.logical_or(available,one_hot.transform([x]).toarray())

    #return np.concatenate((roster[0],available[0]))

    

# This will create the MLP neural network for the "state" half of the Network
def create_mlp():
    # define our MLP model for the "state" half of the network
    #mlp = Sequential()
    #mlp.add(Dense(168, input_dim=336, activation="relu"))
    #mlp.add(Dense(168, input_dim=1, activation="relu"))
    #mlp.add(Dense(84, activation="relu"))

    inputs = Input(shape=(336,))
    layers = Dense(168, activation="relu")(inputs)
    layers = Dense(84, activation="relu")(layers)

    mlp = Model(inputs,layers)

    return mlp


# This will create the CNN for the "Player Data" half of the Network
def create_cnn():
    # define our CNN for the "Player Data" half of the Network
    inputs = Input(shape=(208,))
    layers = Embedding(208,168)(inputs)
    layers = Conv1D(52, kernel_size=208, activation="relu")(layers)
    #layers = BatchNormalization()(layers)
    #layers = MaxPooling1D()(layers)
    #layers = Conv1D(104, kernel_size=, activation="relu")(layers)
    #layers = BatchNormalization()(layers)
    #layers = MaxPooling1D()(layers)
    layers = Flatten()(layers)
    layers = Dense(52, activation="relu")(layers)
    #layers = BatchNormalization()(layers)
    layers = Dropout(0.25)(layers)

    cnn = Model(inputs,layers)
    return cnn


# This will combine the "state" half of the Network and the "Player Data"
# half of the network and combine them. It will then run the combined outputs
# into a Dense and activation layer to create the full Neural Network
def create_model():

    # create the two halves of the network
    mlp = create_mlp()
    cnn = create_cnn()

    # concatenate the outputs of the two halves of the Network
    combinedInput = concatenate([mlp.output, cnn.output])
    
    # final fully connected layers transform the data to the Q values we are interested in
    final_layers = Dense(336, activation="relu")(combinedInput)
    final_layers = Dense(168, activation="relu")(final_layers)

    model = Model(inputs=[mlp.input, cnn.input], outputs=final_layers)
    
    model.compile(loss="mse", optimizer="adam")
    model.summary()
    # try plotting model
    #plot_model(model, to_file='draft/model.png', show_shapes=True)

    return model

# This function will save the trained model to be used by the validation picker
def export_model(model):
    # export the model to be saved for the smart picker during evaluation
    model.save('draft/model.h5')

# This function will be used by the validation picker to import the model if necessary
def import_model():

    # load the previously saved model for the smart picker during evaluation 
    model = load_model('draft/model.h5')
    
    return model

class Picker(object):

    def __init__(self, draft_position, rounds, name, fav_team):

        self.picker_type = "picker"
        self.draft_pos = draft_position
        self.players = []
        self.name = name
        self.fav_team = self.pick_team(fav_team)
        self.starting_lineup = {
                "1": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "2": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "3": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "4": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "5": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "6": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "7": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "8": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "9": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "10": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "11": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "12": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "13": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "14": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "15": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "16": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
                "17": dict(QB=0,RB1=0,RB2=0,WR1=0,WR2=0,TE=0,FLEX=0),
        }
        self.lineup = dict(QB=1, RB=2, WR=2, TE=1, FLEX=1, DEF=1, PK=1, BNCH=rounds-9)
        self.season_points = 0
        for week in range(1,18):
            self.starting_lineup[str(week)]["QB"] = 0
            self.starting_lineup[str(week)]["RB1"] = 0
            self.starting_lineup[str(week)]["RB2"] = 0
            self.starting_lineup[str(week)]["WR1"] = 0
            self.starting_lineup[str(week)]["WR2"] = 0
            self.starting_lineup[str(week)]["TE"] = 0
            self.starting_lineup[str(week)]["FLEX"] = 0


    def pick_team(self, fav_team):
        """ pick a team at random """
        teams = ["none", "PIT", "CIN", "CLE", "BAL", "NYJ", "NE", "BUF", "MIA", "HOU", "JAX", "IND", "TEN", "KC", "LAC", "DEN", "OAK", "SEA", "ARI", "LAR", "SF", "DAL", "PHI", "WAS", "NYG", "CAR", "NO", "TB", "ATL", "MIN", "CHI", "GB", "DET"]
        if fav_team in teams:
            return fav_team
        else:
            return random.choice(teams)

    def factory(picker_type, draft_position, rounds, name, adp_list, q_file, fav_team):
        # this is the facotry to create all the different types of pickers
        if picker_type   == "fanboy": return fanboyPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "value-based": return valuePicker(draft_position, rounds, name, fav_team)
        elif picker_type == "zeroRB": return zeroRBPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "zeroWR": return zeroWRPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "user": return userPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "roster": return rosterPicker(draft_position, rounds, name, fav_team)
        elif picker_type == "TE/QB": return TE_QB_Picker(draft_position, rounds, name, fav_team)
        elif picker_type == "train": return trainer(draft_position, rounds, name, adp_list, fav_team)
        elif picker_type == "smart": return smart_picker(draft_position, rounds, name, q_file, fav_team)
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
        #print("player_index: %s" % player_index)
        #print("distribution: %s" % distribution)
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
        player_index = []
        if len(adp_list.players) > 4:
            player_index = adp_list.players[0:5]
            distribution = [0.2,0.2,0.2,0.2,0.2]
        elif len(adp_list.players) > 3:
            player_index = adp_list.players[0:4]
            distribution = [0.25,0.25,0.25,0.25]
        elif len(adp_list.players) > 2:
            player_index = adp_list.players[0:3]
            distribution = [0.34,0.33,0.33]
        elif len(adp_list.players) > 1:
            player_index = adp_list.players[0:2]
            distribution = [0.5,0.5]
        else:
            player_index = [adp_list.players[0]]
            distribution = [1]

        #distribution = [1/len(player_index) for x in range(len(player_index))]
        pick = self.make_pick(player_index, distribution) 
        adp_list.remove_player(pick['name'])
        self.players.append(pick)
        self.calculate_lineup(pick)
        return pick
        
    def calculate_season_points(self):
        # here we will calculate the total points scored on the season
        self.season_points = 0

        for week in range(1,18):
            self.season_points += self.starting_lineup[str(week)]['QB'] + self.starting_lineup[str(week)]['RB1'] + self.starting_lineup[str(week)]['RB2'] + self.starting_lineup[str(week)]['WR1'] + self.starting_lineup[str(week)]['WR2'] + self.starting_lineup[str(week)]['TE'] + self.starting_lineup[str(week)]['FLEX']

        #print("season points: %s" % self.season_points)

    def calculate_lineup(self, player):
        #print("picking %s" % player['name'])
        name = []
        name = player['name'].split()
        real_name = name[1] + ", " + name[0]

        fantasy_points = pd.read_csv("draft/fantasy_points.csv")
        fantasy_points = fantasy_points[fantasy_points['Name'] == real_name]
        fantasy_points = fantasy_points[fantasy_points['Position'] == player['position']]
        #print("after")
        #print(fantasy_points)
        reward = 0
        #print("Lineup Before Calculate Lineup: %s" % self.starting_lineup)
        for week in range(1,18):
            #print("week %s" % week)
            #print(fantasy_points[fantasy_points['Week'] == week]['Fantasy Points'])
            #print(fantasy_points[fantasy_points['Week'] == week]['Fantasy Points'].values[0])
            if not fantasy_points[fantasy_points['Week'] == week]['Fantasy Points'].empty:
                points = fantasy_points[fantasy_points['Week'] == week]['Fantasy Points'].values[0]
            else:
                points = 0

            #print("points %s" % points)
            #week_data = fantasy_points[fantasy_points['Week'] == week]
            #print(week_data)
            #print(type(week_data))
            #print(week_data['Fantasy Points'].values[0])
            #print(type(week_data['Fantasy Points'].values[0]))
            if player['position'] == "QB":
                if self.starting_lineup[str(week)]['QB'] < points:
                    reward += points - self.starting_lineup[str(week)]['QB']
                    self.starting_lineup[str(week)]['QB'] = points

            elif player['position'] == "WR":
                if self.starting_lineup[str(week)]['WR1'] < points:
                    if self.starting_lineup[str(week)]['WR2'] > self.starting_lineup[str(week)]['FLEX']:
                        reward += points - self.starting_lineup[str(week)]['FLEX']
                        self.starting_lineup[str(week)]['FLEX'] = self.starting_lineup[str(week)]['WR2']
                        self.starting_lineup[str(week)]['WR2'] = self.starting_lineup[str(week)]['WR1']
                        self.starting_lineup[str(week)]['WR1'] = points
                    else:
                        reward += points - self.starting_lineup[str(week)]['WR2']
                        self.starting_lineup[str(week)]['WR2'] = self.starting_lineup[str(week)]['WR1']
                        self.starting_lineup[str(week)]['WR1'] = points

                elif self.starting_lineup[str(week)]['WR2'] < points:
                    if self.starting_lineup[str(week)]['WR2'] > self.starting_lineup[str(week)]['FLEX']:
                        reward += points - self.starting_lineup[str(week)]['FLEX']
                        self.starting_lineup[str(week)]['FLEX'] = self.starting_lineup[str(week)]['WR2']
                        self.starting_lineup[str(week)]['WR2'] = points
                    else:
                        reward += points - self.starting_lineup[str(week)]['WR2']
                        self.starting_lineup[str(week)]['WR2'] = points

                elif self.starting_lineup[str(week)]['FLEX'] < points:
                    reward += points - self.starting_lineup[str(week)]['FLEX']
                    self.starting_lineup[str(week)]['FLEX'] = points

                #print("Lineup Middle: %s" % self.starting_lineup)

            elif player['position'] == "RB":
                if self.starting_lineup[str(week)]['RB1'] < points:
                    if self.starting_lineup[str(week)]['RB2'] > self.starting_lineup[str(week)]['FLEX']:
                        reward += points - self.starting_lineup[str(week)]['FLEX']
                        self.starting_lineup[str(week)]['FLEX'] = self.starting_lineup[str(week)]['RB2']
                        self.starting_lineup[str(week)]['RB2'] = self.starting_lineup[str(week)]['RB1']
                        self.starting_lineup[str(week)]['RB1'] = points
                    else:
                        reward += points - self.starting_lineup[str(week)]['RB2']
                        self.starting_lineup[str(week)]['RB2'] = self.starting_lineup[str(week)]['RB1']
                        self.starting_lineup[str(week)]['RB1'] = points

                elif self.starting_lineup[str(week)]['RB2'] < points:
                    if self.starting_lineup[str(week)]['RB2'] > self.starting_lineup[str(week)]['FLEX']:
                        reward += points - self.starting_lineup[str(week)]['FLEX']
                        self.starting_lineup[str(week)]['FLEX'] = self.starting_lineup[str(week)]['RB2']
                        self.starting_lineup[str(week)]['RB2'] = points
                    else:
                        reward += points - self.starting_lineup[str(week)]['RB2']
                        self.starting_lineup[str(week)]['RB2'] = points

                elif self.starting_lineup[str(week)]['FLEX'] < points:
                    reward += points - self.starting_lineup[str(week)]['FLEX']
                    self.starting_lineup[str(week)]['FLEX'] = points
                #print("Lineup Middle: %s" % self.starting_lineup)

            elif player['position'] == "TE":
                if self.starting_lineup[str(week)]['TE'] < points:
                    if self.starting_lineup[str(week)]['TE'] > self.starting_lineup[str(week)]['FLEX']:
                        reward += points - self.starting_lineup[str(week)]['FLEX']
                        self.starting_lineup[str(week)]['FLEX'] = self.starting_lineup[str(week)]['TE']
                        self.starting_lineup[str(week)]['TE'] = points
                    else: 
                        reward += points - self.starting_lineup[str(week)]['TE']
                        self.starting_lineup[str(week)]['TE'] = points

                elif self.starting_lineup[str(week)]['FLEX'] < points:
                    reward += points - self.starting_lineup[str(week)]['FLEX']
                    self.starting_lineup[str(week)]['FLEX'] = points

        #print("Lineup After Calculate Lineup: %s" % self.starting_lineup)
        self.calculate_season_points()
        return reward


        

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
        player_index = []
        for x in adp_list.players:
            if x['team'] == self.fav_team:
                team_players.append(x)

        if len(adp_list.players) >= 5:
            player_index.append(adp_list.players[0])
            player_index.append(adp_list.players[1])
            player_index.append(adp_list.players[2])
            player_index.append(adp_list.players[3])
            if not team_players:
                player_index.append(adp_list.players[4])
            else:
                player_index.append(team_players[0])
        #print(player_index)
            distribution = [0.225,0.225,0.225,0.225,0.1]
        else:
            player_index = adp_list.players
            distribution = [1.0/len(player_index) for x in range(len(player_index))]

        if len(player_index) == 0:
            player_index.append(adp_list.players[0])
            distribution = [1]
        pick = super(fanboyPicker, self).make_pick(player_index, distribution)
        #print(pick['name'])
        adp_list.remove_player(pick['name'])
        self.players.append(pick)
        super(fanboyPicker, self).calculate_lineup(pick)
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
        player_index = []
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
            player_index.append(wrs[0])
            player_index.append(wrs[1])
            player_index.append(wrs[2])
            player_index.append(qbs[0])
            player_index.append(tes[0])
            distribution = [0.25,0.25,0.25,0.125,0.125]
        elif len(self.players) < 8:
            if len(rbs) > 2:
                player_index.append(rbs[0])
                player_index.append(rbs[1])
                player_index.append(rbs[2])
            elif len(rbs) > 1:
                player_index.append(rbs[0])
                player_index.append(rbs[1])
            elif len(rbs) > 0:
                player_index.append(rbs[0])

            if len(wrs) > 0:
                player_index.append(wrs[0])
            if len(qbs) > 0:
                player_index.append(qbs[0])
            if len(tes) > 0:
                player_index.append(tes[0])
            distribution = [1/len(player_index) for x in range(len(player_index))]
        elif len(self.players) < 12:
            # conditional here to pick up what we dont have?
            player_index = []

            if len(wrs) > 1:
                player_index.append(wrs[0])
                player_index.append(wrs[1])
            elif len(wrs) > 0:
                player_index.append(wrs[0])

            if len(qbs) > 0:
                player_index.append(qbs[0])
            if len(rbs) > 0:
                player_index.append(rbs[0])
            if len(tes) > 0:
                player_index.append(tes[0])
            distribution = [1.0/len(player_index) for x in range(len(player_index))]
        else:
            player_index = defk
            if len(qbs) > 0:
                player_index.append(qbs[0])
            if len(rbs) > 0:
                player_index.append(rbs[0])
            if len(tes) > 0:
                player_index.append(tes[0])
            distribution = [1.0/len(player_index) for x in range(len(player_index))]
            
        if len(player_index) == 0:
            player_index.append(adp_list.players[0])
            distribution = [1]
        pick = super(zeroRBPicker, self).make_pick(player_index, distribution)
        adp_list.remove_player(pick['name'])
        self.players.append(pick)
        super(zeroRBPicker, self).calculate_lineup(pick)
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
        player_index = []
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
            player_index.append(rbs[0])
            player_index.append(rbs[1])
            player_index.append(rbs[2])
            player_index.append(qbs[0])
            player_index.append(tes[0])
            distribution = [0.25,0.25,0.25,0.125,0.125]
        elif len(self.players) < 8:
            if len(wrs) > 2:
                player_index.append(wrs[0])
                player_index.append(wrs[1])
                player_index.append(wrs[2])
            elif len(wrs) > 1:
                player_index.append(wrs[0])
                player_index.append(wrs[1])
            elif len(wrs) > 0:
                player_index.append(wrs[0])

            if len(rbs) > 0:
                player_index.append(rbs[0])
            if len(qbs) > 0:
                player_index.append(qbs[0])
            if len(tes) > 0:
                player_index.append(tes[0])
            distribution = [1/len(player_index) for x in range(len(player_index))]
        elif len(self.players) < 12:
            # conditional here to pick up what we dont have?
            if len(wrs) > 1:
                player_index.append(wrs[0])
                player_index.append(wrs[1])
            elif len(wrs) > 0:
                player_index.append(wrs[0])

            if len(qbs) > 0:
                player_index.append(qbs[0])
            if len(rbs) > 0:
                player_index.append(rbs[0])
            if len(tes) > 0:
                player_index.append(tes[0])
            distribution = [1.0/len(player_index) for x in range(len(player_index))]
        else:
            player_index = defk
            if len(qbs) > 0:
                player_index.append(qbs[0])
            if len(rbs) > 0:
                player_index.append(rbs[0])
            if len(tes) > 0:
                player_index.append(tes[0])
            distribution = [1.0/len(player_index) for x in range(len(player_index))]
            
        if len(player_index) == 0:
            player_index.append(adp_list.players[0])
            distribution = [1]
        pick = super(zeroWRPicker, self).make_pick(player_index, distribution)
        adp_list.remove_player(pick['name'])
        self.players.append(pick)
        super(zeroWRPicker, self).calculate_lineup(pick)
        return pick



##################################################################
# class to simulate a drafter that prioritizes QBs and TEs       #
##################################################################
class TE_QB_Picker(Picker):


    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(TE_QB_Picker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "TE/QB"
        self.te = []
        self.qb = []

    def think(self, adp_list):
        # seperate player list into positions
        rbs  = []
        qbs  = []
        wrs  = []
        tes  = []
        defk = []
        player_index = []
        distribution = []
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
            if not self.te and not self.qb:
                player_index.append(tes[0])
                player_index.append(tes[1])
                player_index.append(qbs[0])
                player_index.append(qbs[1])
                player_index.append(rbs[0])
                player_index.append(wrs[0])
                distribution = [0.2,0.2,0.2,0.2,0.1,0.1]
            elif not self.te:
                player_index.append(tes[0])
                player_index.append(tes[1])
                player_index.append(rbs[0])
                player_index.append(wrs[0])
                distribution = [0.4,0.4,0.1,0.1]
            elif not self.qb:
                player_index.append(qbs[0])
                player_index.append(qbs[1])
                player_index.append(rbs[0])
                player_index.append(wrs[0])
                distribution = [0.4,0.4,0.1,0.1]
            else:
                player_index.append(rbs[0])
                player_index.append(rbs[1])
                player_index.append(wrs[0])
                player_index.append(wrs[1])
                distribution = [0.25, 0.25, 0.25, 0.25]

        elif len(self.players) < 12:
            if not self.te and not self.qb:
                if len(tes) > 1:
                    player_index.append(tes[0])
                    player_index.append(tes[1])
                elif len(tes) > 0: 
                    player_index.append(tes[0])

                if len(qbs) > 1:
                    player_index.append(qbs[0])
                    player_index.append(qbs[1])
                elif len(qbs) > 0:
                    player_index.append(qbs[0])

            elif not self.te:
                if len(tes) > 1:
                    player_index.append(tes[0])
                    player_index.append(tes[1])
                elif len(tes) > 0:
                    player_index.append(tes[0])

            elif not self.qb:
                if len(qbs) > 1:
                    player_index.append(qbs[0])
                    player_index.append(qbs[1])
                elif len(qbs) > 0:
                    player_index.append(qbs[0])

            else:
                if len(rbs) > 1:
                    player_index.append(rbs[0])
                    player_index.append(rbs[1])
                elif len(rbs) > 0:
                    player_index.append(rbs[0])

                if len(wrs) > 1:
                    player_index.append(wrs[0])
                    player_index.append(wrs[1])
                elif len(wrs) > 0:
                    player_index.append(wrs[0])

            distribution = [1.0/len(player_index) for x in range(len(player_index))]
        else:
            player_index = defk
            if len(qbs) > 0:
                player_index.append(qbs[0])
            if len(wrs) > 0:
                player_index.append(wrs[0])
            if len(tes) > 0:
                player_index.append(tes[0])

            if len(player_index) == 0:
                player_index.append(adp_list.players[0])
            distribution = [1.0/len(player_index) for x in range(len(player_index))]

        if len(player_index) == 0:
            player_index.append(adp_list.players[0])
            distribution = [1]
        pick = super(TE_QB_Picker, self).make_pick(player_index, distribution)
        adp_list.remove_player(pick['name'])
        self.players.append(pick)
        if pick['position'] == 'QB':
            self.qb.append(pick)
        if pick['position'] == 'TE':
            self.te.append(pick)
        super(TE_QB_Picker, self).calculate_lineup(pick)
        return pick



############################################################
# class to implement reinforcement learning neural network #
# algorithm.                                               #
############################################################
class userPicker(Picker):


    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(userPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "user"
        # need to initialize variables. Q matrix? 

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
        # seperate player list into positions
        rbs  = []
        qbs  = []
        wrs  = []
        tes  = []
        defk = []
        player_index = []
        distribution = []
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

        if self.lineup['QB'] > 0:
                if len(qbs) > 1:
                        player_index.append(qbs[0])
                        player_index.append(qbs[1])
                elif len(qbs) > 0:
                        player_index.append(qbs[0])

        if self.lineup['RB'] > 0:
                if len(rbs) > 1:
                        player_index.append(rbs[0])
                        player_index.append(rbs[1])
                elif len(rbs) > 0:
                        player_index.append(rbs[0])

        if self.lineup['WR'] > 0:
                if len(wrs) > 1:
                        player_index.append(wrs[0])
                        player_index.append(wrs[1])
                elif len(wrs) > 0:
                        player_index.append(wrs[0])

        if self.lineup['TE'] > 0:
                if len(tes) > 1:
                        player_index.append(tes[0])
                        player_index.append(tes[1])
                elif len(tes) > 0:
                        player_index.append(tes[0])

        if self.lineup['QB'] == 0 and self.lineup['RB'] == 0 and self.lineup['WR'] == 0 and self.lineup['TE'] == 0:
                if len(qbs) > 1:
                        player_index.append(qbs[0])
                        player_index.append(qbs[1])
                elif len(qbs) > 0:
                        player_index.append(qbs[0])
                
                if len(rbs) > 1:
                        player_index.append(rbs[0])
                        player_index.append(rbs[1])
                elif len(rbs) > 0:
                        player_index.append(rbs[0])
                
                if len(wrs) > 1:
                        player_index.append(wrs[0])
                        player_index.append(wrs[1])
                elif len(wrs) > 0:
                        player_index.append(wrs[0])

                if len(tes) > 1:
                        player_index.append(tes[0])
                        player_index.append(tes[1])
                elif len(tes) > 0:
                        player_index.append(tes[0])

        if len(player_index) == 0:
            player_index.append(adp_list.players[0])
        distribution = [1.0/len(player_index) for x in range(len(player_index))]

        pick = super(rosterPicker, self).make_pick(player_index, distribution)
        adp_list.remove_player(pick['name'])
        self.players.append(pick)
        super(rosterPicker, self).calculate_lineup(pick)
        return pick

#########################################################################
# class to train the reinforcement learning neural network to create    #
# the appropriate Q-matrix                                              #
#########################################################################
class trainer(Picker):

    def __init__(self, draft_postion, rounds, name, adp_list, fav_team=''):

        super(trainer, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "trainer"
        self.full_adp = adp_list.players
        self.nn = create_model()
        self.Q = dict()
        self.y = 0.95
        self.eps = 0.5
        self.decay_factor = 0.999
        self.player_data = pre_process_player_data(self.full_adp)

    def think(self, adp_list):
        # here is where the machine learning actually takes place
        self.eps *= self.decay_factor
        q = []
        done = False
        r_sum = 0
        state_data = pre_process_state_data(self.players, adp_list.players, self.full_adp)
        print("STATE DATA = %s" % state_data.T)
        #print("len(state_data) = %s" % len(state_data))
        #print("type(state_data) = %s" % type(state_data))
        #print("type(state_data[0] = %s" % type(state_data[0]))
        #print("state_data.shape = %s" % state_data.shape)
        #print(type(self.player_data))
        q = self.nn.predict([state_data.T,self.player_data.values])
        # finish ranking data 
        if np.random.random() < self.eps:
            random_pick = np.random.choice([adp_list.players[0]],[1])
            pick_index = self.full_adp.index(random_pick)
        else:
            ranks = ss.rankdata(q,method='min')
            pick_index = np.argmax(ranks)
            while not self.full_adp[pick_index] in adp_list.players:
                q[pick_index] = 0
                ranks = ss.rankdata(q,method='min')
                pick_index = np.argmax(ranks)

        pick = super(trainer, self).make_pick([self.full_adp[pick_index]],[1])
        adp_list.remove_player(pick['name'])
        self.players.append(pick)
        reward = super(trainer, self).calculate_lineup(pick)

        new_state_data = pre_process_state_data(self.players, adp_list.players, self.full_adp)
        new_q = reward + self.y * np.argmax(self.nn.predict([new_state_data.T, self.player_data]))
        q[0][pick_index] = new_q

        print(q)
        print(q.shape)
        print(type(q))
        self.nn.fit(x={ "input_1": state_data.T, "input_2": self.player_data}, y=q, epochs=1, verbose=0)
        self.Q.append({str(state_data.to_numpy()): q})
        return pick


##########################################################################
# class to import a trained Q-matrix and pick based off a trained neural #
# network                                                                #
##########################################################################
class smart_picker(Picker):

    def __init__(self, draft_postion, rounds, name, q_file, fav_team=''):

        super(smart_picker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "smart"
        self.Q = pd.read_csv(q_file)


    def think(self, adp_list):
        # here I need to just read the read the Q matrix and pick the highest value player
        return super(smart_picker, self).think(adp_list)


