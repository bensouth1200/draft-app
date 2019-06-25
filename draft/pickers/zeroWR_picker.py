from draft import picker

class zeroWRPicker(picker.Picker):

    # class to simulate a drafter using the zero WR strategy

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(zeroWRPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "zero WR"

    def think():
	pass
