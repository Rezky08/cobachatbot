# import tensorflow as tf
import random
import numpy as np
import filepath
import json
from preprocessing.text_preprocessing import Preprocessing

class model_handle:
    def __init__(self,model,name):
        self.name = name
        self.model = model
        self.bag_words = None
        self.labels = None
        self.answers =None
        self.preprocessing = Preprocessing()

    def load_data(self):
        with open(filepath.path('/model/{}/params.json'.format(self.name)), 'r') as file:
            params = json.load(file)
        self.bag_words = params['bag_words']
        self.labels = params['labels']
        self.answers = params['answers']

    def _prep_text(self,text):
        text = self.preprocessing.repair_slangword(text)
        text = self.preprocessing.stemmer.stem(text)
        text_tokenized = self.preprocessing.word_tokenizing(text)
        return text_tokenized

    def _to_input(self,text):
        text_tokenized = self.preprocessing.text_preprocessing(text)
        x_input = []
        for index, item in enumerate(self.bag_words):
            x_input.append(text_tokenized.count(item))
        return x_input

    def get_answer(self,text):
        x_input = np.array([self._to_input(text)])
        res = self.model.predict(x_input)[0]
        res_index = np.argmax(res)
        if res[res_index] < .7:
            return "maaf, saya belum memahami apa yang kamu bicarakan. nanti saya akan belajar lagi"
        label_id = self.labels[res_index][0]
        ans_index = np.where(np.array(self.answers)[:,1]=='{}'.format(label_id))
        ans = np.array(self.answers)[ans_index][:,0]
        select_ans = random.choice(ans)
        return select_ans
