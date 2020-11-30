import json
import string
import filepath
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Preprocessing:
    def __init__(self):
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()
        with open(filepath.path('/preprocessing/slangwords.json')) as f:
            self.slangwords=json.load(f)
            self.slangwords={"slang":list(self.slangwords['slang'].values()),"formal":list(self.slangwords['formal'].values())}
        with open(filepath.path('/preprocessing/stopwords-id.json')) as f:
            self.stopwords=json.load(f)
        self.text_dummy = "Bahasa Indonesia adalah bahasa resmi Republik Indonesia[1] dan bahasa persatuan bangsa Indonesia.[2] Bahasa Indonesia diresmikan penggunaannya setelah Proklamasi Kemerdekaan Indonesia, tepatnya sehari sesudahnya, bersamaan dengan mulai berlakunya konstitusi. Di Timor Leste, bahasa Indonesia berstatus sebagai bahasa kerja. "

    # Step 1 Casefolding
    def casefolding(self,text):
        # lowercase
        text = text.lower()
        # hapus angka
        text = text.translate(str.maketrans(string.digits,' '*len(string.digits)))
        # hapus tanda baca
        text = text.translate(str.maketrans(string.punctuation,' '*len(string.punctuation)))
        # hapus whitespace
        text = text.strip(" ")
        return text

    # Step 2 Tokenizing
    def word_tokenizing(self,text):
        # Tokenizing Kata
        text = self.casefolding(text)
        return text.split()
    def sentence_tokenizing(self,text):
        # Tokenizing kalimat
        text = text.split(".")
        for index,item in enumerate(text):
            text[index] = self.word_tokenizing(item)
        return text
    # Step 3 Filtering
    def stopword_remover(self,text):
        if type(text) == str:
            text = self.casefolding(text)
            text = text.split()
        text = [word for word in text if word not in self.stopwords]
        text = " ".join(text)
        return text
    def repair_slangword(self,text):
        text = self.word_tokenizing(text)
        for index,item in enumerate(text):
            if item in self.slangwords['slang']:
                slang_index = self.slangwords['slang'].index(item)
                text[index] = self.slangwords['formal'][slang_index]
        text = " ".join(text)
        return text
    def text_preprocessing(self,text):
        repaired = self.repair_slangword(text)
        repaired = self.stopword_remover(repaired)
        repaired = self.stemmer.stem(repaired)
        tokenized = self.word_tokenizing(repaired)
        return tokenized
