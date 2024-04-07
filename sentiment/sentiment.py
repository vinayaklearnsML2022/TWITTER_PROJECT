from transformers import pipeline
import torch



def classifier(text):
    # classify = pipeline("sentiment-analysis",model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    classify = pipeline("sentiment-analysis",model="cardiffnlp/xlm-twitter-politics-sentiment")
    res = classify(text)
   
    return res

