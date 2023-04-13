
class par:
    def __init__(self):
        self.a = 'dsadsda'


class son(par):
    def __init__(self):
        par.__init__(self)

    def s(self):
      print(self.a)



son().s()      