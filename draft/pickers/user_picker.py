from picker import Picker

class userPicker(Picker):

    """ class to let user pick in draft """

    def __init__(self, draft_postion, rounds, fav_team):

        super.__init__(draft_postion, rounds, super.pick_team(fav_team))
        self.picker_type = "user"

    def think():

