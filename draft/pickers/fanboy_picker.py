import draft
import draft.picker as dp
#from draft import picker
print(help('modules draft'))

class fanboyPicker(dp.Picker):

    # class to simulate a fanboy drafter. Players on the picker's
    # favorite team will be overvalued 

    def __init__(self, draft_postion, rounds, name, fav_team=''):

        super(fanboyPicker, self).__init__(draft_postion, rounds, name, fav_team)
        self.picker_type = "fanboy"

    def think():
	super(fanboyPicker, self).think()
