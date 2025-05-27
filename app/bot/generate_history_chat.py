

class Chat:
    def __init__(self, contents:dict):
        self.contents = contents

    def addContent(self, **kwarg) :
        role = kwarg.get("role") 
        content = kwarg.get("content")

        
        
