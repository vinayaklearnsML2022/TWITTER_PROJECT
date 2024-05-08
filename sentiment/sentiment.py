from transformers import pipeline
import torch
import re




def sentiment(text):
    classify = pipeline("sentiment-analysis",model="cardiffnlp/xlm-twitter-politics-sentiment")
    res = classify(text)
    return "".join(map(str, re.findall("'label': '(.*?)'",str(res))))

