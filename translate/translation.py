import deep_translator
from deep_translator import GoogleTranslator


class Translation:

    def __init__(self,text):
        self.text=text

    def google(self):
        eng = GoogleTranslator(source='auto').translate(self.text)[:1000]
        return eng

