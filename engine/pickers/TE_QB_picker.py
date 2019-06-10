import picker

class TE_QB_Picker(Picker):

    # class to simulate a drafter that prioritizes QBs and TEs 

    def __init__(self, draft_postion, rounds, fav_team):

        super.__init__(draft_postion, rounds, super.pick_team(fav_team))
        self.picker_type = "TE/QB"

    def think():

