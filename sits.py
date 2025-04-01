from kivy.uix.label import Label
from kivy.clock import Clock

class Sits(Label):
    
    def __init__(self, total, **kwargs):
        self.now = 0
        self.total = 30

        my_text = 'Осталось приседаний: ' + str(self.total)
        super().__init__(text=my_text, **kwargs)

    def next(self, *args):
        self.now += 1
        quantity = max(0,self.total - self.now)
        my_text = 'Осталось приседаний: ' + str(quantity)
        self.text =my_text
