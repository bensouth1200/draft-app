from sklearn.preprocessing import OneHotEncoder
from keras.models import Sequential
from keras.models import Model
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import AveragePooling1D
from keras.layers import Flatten
from keras.layers import Input
from keras.layers import concatenate
from keras.utils import plot_model
from keras.models import load_model
import numpy as np
import pandas as pd

# this function will read in player data from the ADP List and 
# do some preprocessing to get it ready to pass to the CNN
def pre_process_player_data(full_adp_list):
    # convert the adp_list from a list of dicts to a pandas dataframe 
    all_players = pd.DataFrame(all_players,columns=['name','adp','times_drafted','team','high','low','adp_formatted','player_id','position','bye','stdev'])

    encoded_cols = ['name','team','position']
    encoder = OneHotEncoder(handle_unknown='ignore')
    encoded_data = encoder.fit_transform(all_players[encoded_cols]).toarray()
    encoded_data = pd.DataFrame(encoded_data,columns=encoder.get_feature_names(['name','team','position']))

    return pd.concat([all_players['adp'],all_players['bye'],encoded_data],axis=1,sort=False)

    
# this function will read in the current state of the draft and encode 
# is into an input vector for the MLP
def pre_process_state_data(team_roster, available_players, full_adp_list):
    
    # fit a OneHotEncoder to the player names
    one_hot = OneHotEncoder(handle_unknown='ignore')
    player_names = [x['name'] for x in full_adp_list]
    one_hot.fit(player_names)

    # grab just the names of the players in both roster and available players
    team_names = [x['name'] for x in team_roster]
    available_names = [x['name'] for x in available_players]

    # now create one hot encoded array for the roster
    roster = np.zeros(len(full_adp_list))
    for x in team_names:
        roster = np.logical_or(roster,one_hot.transform([x]).toarray())

    # create one hot encoded array for the available players
    available = np.zeros(len(full_adp_list))
    for x in available_players:
        available = np.logical_or(available,one_hot.transform([x]).toarray())

    return np.concatenate((roster[0],available[0]))

    

# This will create the MLP neural network for the "state" half of the Network
def create_mlp():
    # define our MLP model for the "state" half of the network
    mlp = Sequential()
    mlp.add(Dense(168, input_dim=336, activation="relu"))
    mlp.add(Dense(84, activation="relu"))

    return mlp

# This will create the CNN for the "Player Data" half of the Network
def create_cnn():
    # define our CNN for the "Player Data" half of the Network
    inputs = Input(shape=209)
    layers = Conv1D(64, (1,208), activation="relu")(inputs)
    layers = BatchNormalization()(layers)
    layers = AveragePooling1D(pool_size=2)(layers)
    layers = Conv1D(128, (1,104), activation="relu")(layers)
    layers = BatchNormalization()(layers)
    layers = AveragePooling1D(pool_size=2)(layers)
    layers = Flatten()(layers)
    layers = Dense(52, activation="relu")(layers)
    layers = BatchNormalization()(layers)
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
    # try plotting model
    plot_model(model, to_file='draft/model.png', show_shapes=True)

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
