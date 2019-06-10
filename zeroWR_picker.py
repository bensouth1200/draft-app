import picker

class zeroWRPicker(Picker):

    """ class to let user pick in draft """

    def __init__(self, draft_postion, players, fav_team):

        super.__init__(draft_postion, "", super.pick_team())
        self.picker_type = "zero WR"

    def think():

