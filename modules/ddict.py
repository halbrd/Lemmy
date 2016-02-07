class ddict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self['_attributes'] = dict()
        self.allowDotting()
    def allowDotting(self, state=True):
        if state:
            self.update(self['_attributes'])
            self.__dict__ = self
        else:
            self.__dict__ = self['_attributes']