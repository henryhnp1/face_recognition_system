class SessionControl:
    __instance = None
    @staticmethod
    def get_instance():
        if SessionControl.__instance == None:
            SessionControl()
        return SessionControl.__instance
    
    def __init__(self, user=None):
        if SessionControl.__instance != None:
            raise Exception('')
        else:
            SessionControl.__instance = self
            self.user = user