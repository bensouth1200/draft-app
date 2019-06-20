import picker

class rosterPicker(Picker):

    # class to simulate a roster-based approach to drafting.
    # this drafter will prioritize filling open roster spots to bench spots

    def __init__(self, draft_postion, rounds, fav_team):

        super.__init__(draft_postion, rounds, super.pick_team(fav_team))
        self.picker_type = "roster"

    def think():

