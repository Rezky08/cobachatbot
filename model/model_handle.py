# import tensorflow as tf
import random
import numpy as np
import filepath
import json
from preprocessing.text_preprocessing import Preprocessing


bag_words = None
labels = None
answers =None
preprocessing = Preprocessing()

def load_data():
    global bag_words,labels,answers
    with open(filepath.path('/model/params.json'), 'r') as file:
        params = json.load(file)
    bag_words = params['bag_words']
    labels = params['labels']
    answers = params['answers']

def _prep_text(text):
    global preprocessing
    text = preprocessing.repair_slangword(text)
    text = preprocessing.stemmer.stem(text)
    text_tokenized = preprocessing.word_tokenizing(text)
    return text_tokenized

def _to_input(text):
    global bag_words
    text_tokenized = _prep_text(text)
    x_input = []
    for index, item in enumerate(bag_words):
        x_input.append(text_tokenized.count(item))
    return x_input

def get_answer(model,text):
    x_input = np.array([_to_input(text)])
    res = model.predict(x_input)[0]
    res_index = np.argmax(res)
    if res[res_index] < .7:
        return "maaf, saya belum memahami apa yang kamu bicarakan. nanti saya akan belajar lagi"

    label_id = labels[res_index][0]
    ans_index = np.where(np.array(answers)[:,2]=='{}'.format(label_id))
    ans = np.array(answers)[ans_index][:,1]
    select_ans = random.choice(ans)
    return select_ans
