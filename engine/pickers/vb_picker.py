import picker

class valuePicker(Picker):

    # class to simulate a value-based draft strategy

    def __init__(self, draft_postion, rounds, fav_team):

        super.__init__(draft_postion, rounds, super.pick_team(fav_team))
        self.picker_type = "value-based"

    def think():

