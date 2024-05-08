import re

class Conversion:
    def __init__(self,stri):
        self.stri=stri
    
    def unicode(self):
        return [ord(i) for i in self.stri]


    def extraction_username(self):
        return "".join(map(str, re.findall("RT @(.*?):",self.stri)))
