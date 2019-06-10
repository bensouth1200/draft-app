import picker

class zeroWRPicker(Picker):

    # class to simulate a drafter using the zero WR strategy

    def __init__(self, draft_postion, rounds, fav_team):

        super.__init__(draft_postion, rounds, super.pick_team(fav_team))
        self.picker_type = "zero WR"

    def think():

