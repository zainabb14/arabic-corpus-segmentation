import pyarabic.arabrepr
from tashaphyne.stemming import ArabicLightStemmer

def get_root(data):
    arepr = pyarabic.arabrepr.ArabicRepr()
    ArListem = ArabicLightStemmer() 
    ArListem.light_stem(data)
    return ArListem.get_root()
