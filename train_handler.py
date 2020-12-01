import pandas as pd
import numpy as np
from preprocessing.text_preprocessing import Preprocessing
from sklearn.preprocessing import MinMaxScaler
from model import MLP_model as mlp
import filepath
import json
import sys

class train_handler():
    def __init__(self,questions,answers,labels):
        self.questions = pd.DataFrame(questions).to_numpy()
        self.answers = pd.DataFrame(answers).to_numpy()
        self.labels = pd.DataFrame(labels).to_numpy()
        self.labels_trans = {'{}'.format(item):index for index,item in enumerate(self.labels[:,0])}
        self.labels_index = [index for index,item in enumerate(self.labels)]
        self.bag_words = []
        self.x = []
        self.y = []
        self.preprocessing = Preprocessing()

    def prep_text(self,text):
        text = self.preprocessing.repair_slangword(text)
        text = self.preprocessing.stemmer.stem(text)
        text_tokenized = self.preprocessing.word_tokenizing(text)
        return text_tokenized
    def to_input(self,text_tokenized):
        x_input = []
        for index,item in enumerate(self.bag_words):
            x_input.append(text_tokenized.count(item))
        return x_input

    def save_params(self):
        params = {
                  "bag_words" : self.bag_words,
                  "labels_trans" : self.labels_trans,
                  "questions" : self.questions.tolist(),
                  "answers" : self.answers.tolist(),
                  "labels" : self.labels.tolist()
                }
        with open(filepath.path('/model/params.json'),'w') as file:
            json.dump(params,file)

    def predict(self,model,text):
        text_tokenized = self.prep_text(text)
        x_input = self.to_input(text_tokenized)
        x_input = np.array([x_input])
        res = model.predict(x_input)[0]
        # get answer
        answer_id = self.labels[res.argmax()][0]
        answer_index =  np.where(self.answers[:,2] == '{}'.format(answer_id))
        answers = self.answers[answer_index][:,1]

    def add_to_bagwords(self):
        question_texts = self.questions[:, 1].tolist()
        question_labels = self.questions[:,2].tolist()
        for index,item in enumerate(question_texts):
            text_tokenized = self.prep_text(item)
            self.x.append(text_tokenized)
            self.y.append(question_labels[index])
            self.bag_words.extend(text_tokenized)
        self.bag_words = np.unique(self.bag_words).tolist()

    def train(self):
        self.add_to_bagwords()
        y_train = [self.labels_trans[item] for item in self.y]
        y_train = np.array(y_train)

        x_train = []
        for item in self.x:
            x_train.append(self.to_input(item))
        scaler = MinMaxScaler()
        x_train = scaler.fit_transform(x_train)

        x_test = x_train[::-1]
        y_test = y_train[::-1]

        model = mlp.create_model(x_train[0], [len(x_train[0]) * 2, round(len(self.labels) * 2), round(len(self.labels) * 1.1)],
                                 self.labels_index)
        # model.fit(x_train,y)
        model_name = 'chatbot-model'
        model = mlp.train_model(model, x_train, y_train, x_test, y_test)
        mlp.save_model(model, model_name)
        self.save_params()
        return model

