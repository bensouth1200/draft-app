from draft import picker

class TE_QB_Picker(picker.Picker):

    # class to simulate a drafter that prioritizes QBs and TEs 

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(TE_QB_Picker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "TE/QB"

    def think():
	pass
