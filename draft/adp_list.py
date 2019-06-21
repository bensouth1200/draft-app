import requests
import json
import urllib3

class ADPList():

    # class representing the ADP list of a draft 
    def __init__(self, year, teams, draft_format):

	urllib3.disable_warnings()        
        response = requests.get("https://fantasyfootballcalculator.com/api/v1/adp/" + str(draft_format) + "?teams=" + str(teams) + "&year=" + str(year))
        data = json.loads(response.text)
        self.players = data['players']

    # this will remove the player from the adp list
    def remove_player(self, player_name):
	self.players = [x for x in self.players if x['name'] != player_name]
        
