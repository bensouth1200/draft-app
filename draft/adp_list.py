import requests
import json

class ADPList():

    # class representing the ADP list of a draft 
    def __init__(year, teams, draft_format):
        
        response = requests.get("https://fantasyfootballcalculator.com/api/v1/adp/" + str(draft_format) + "?teams=" + str(teams) + "&year=" + str(year))
        data = json.loads(response.text)
        self.players = data['players']

    # this will remove the player from the adp list
    def remove_player(player_name):
	self.players = [x for x in self.players if x['name'] != player_name]

