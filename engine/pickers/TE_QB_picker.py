import picker

class TE_QB_Picker(Picker):

    """ class to let user pick in draft """

    def __init__(self, draft_postion, players, fav_team):

        super.__init__(draft_postion, "", super.pick_team())
        self.picker_type = "TE/QB"

    def think():

