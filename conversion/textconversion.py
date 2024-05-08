import re


    
def unicode(stri):
        return [ord(i) for i in stri]


def extraction_username(stri):
        return "".join(map(str, re.findall("RT @(.*?):",stri)))
