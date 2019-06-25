from draft import picker

class zeroRBPicker(picker.Picker):

    # class to simulate a drafter using the zero RB strategy

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(zeroRBPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "zero RB"

    def think():
	pass
