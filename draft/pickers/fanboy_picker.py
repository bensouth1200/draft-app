import picker

class fanboyPicker(Picker):

    # class to simulate a fanboy drafter. Players on the picker's
    # favorite team will be overvalued 

    def __init__(self, draft_postion, rounds, fav_team=''):

        super.__init__(draft_postion, rounds, super.pick_team(fav_team))
        self.picker_type = "fanboy"

    def think():

