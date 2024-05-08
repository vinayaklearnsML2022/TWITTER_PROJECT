from transformers import pipeline
import torch
import re



class classifier:

    def __init__(self,text):
        self.text=text

    def sentiment(self):
        classify = pipeline("sentiment-analysis",model="cardiffnlp/xlm-twitter-politics-sentiment")
        res = classify(self.text)
        return "".join(map(str, re.findall("'label': '(.*?)'",str(res))))

