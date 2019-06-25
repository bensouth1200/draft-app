from draft import picker

class valuePicker(picker.Picker):

    # class to simulate a value-based draft strategy

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(valuePicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "value-based"

    def think():
	pass
