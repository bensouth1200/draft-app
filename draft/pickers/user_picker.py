from draft import picker

class userPicker(picker.Picker):

    """ class to let user pick in draft """

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(userPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "user"

    def think():
	pass
