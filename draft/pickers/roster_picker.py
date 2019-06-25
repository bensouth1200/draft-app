from draft import picker

class rosterPicker(picker.Picker):

    # class to simulate a roster-based approach to drafting.
    # this drafter will prioritize filling open roster spots to bench spots

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(rosterPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "roster"

    def think():
	pass
