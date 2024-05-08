import deep_translator
from deep_translator import GoogleTranslator




def google(text):
    eng = GoogleTranslator(source='auto').translate(text)[:1000]
    return eng

