from flask import Flask,request,jsonify
import json
from telebot import apihelper
import cerberus
import requests
from train_handler import train_handler
import pandas as pd
from model import MLP_model as mlp
from model.model_handle import model_handle
from preprocessing.text_preprocessing import Preprocessing
import sys
import os

app = Flask(__name__)

token = 'base64:ifkdAeUN445sfAuVslc+b8/x5VQIfk2z7Wf0ZPJtzUA='
resource_url = "http://cupbotresources.herokuapp.com/api"

def check_token(field,value,error):
    global token
    if not value == token:
        error(field, "is not valid")

def send_message_api_resources(content):
    global resource_url
    return requests.post(url='{}/chat'.format(resource_url), data=content, headers={'Accept':'Application/json'})

@app.route('/text_preprocessing',methods=['POST'])
def preprocessing_text():
    content = request.json

    # validation
    schema = {
        'token': {'required': True, 'check_with': check_token},
        'questions': {'required': True},
    }
    validator = cerberus.Validator(schema)
    if not validator.validate(content):
        return jsonify(validator.errors), 400

    # Preprocessing process
    preprocessing = Preprocessing()
    for index,item in enumerate(content['questions']):
        text = preprocessing.text_preprocessing(item['text'])
        content['questions'][index]['text'] = " ".join(text)
    return jsonify(content)


@app.route('/getChat',methods=['POST'])
def get_answer():
    content = request.json

    # validation
    schema = {
        'id': {'required':True},
        'token':{'required':True,'check_with':check_token},
        'text':{'required':True},
    }
    validator = cerberus.Validator(schema)
    if not validator.validate(content):
        return jsonify(validator.errors),400

    user_chat = {
        'id': content['id'],
        'text': content['text'],
    }
    model = mlp.load_model(user_chat['id'])
    mh = model_handle(model,user_chat['id'])
    mh.load_data()
    if model is None:
        message = "Mohon maaf, kami belum siap untuk menerima pesan"
        response = {
            'ok' : False,
            'message' : message
        }
        return jsonify(response),503
    else:
        message = mh.get_answer(user_chat['text'])
        response = {
            'ok':True,
            'message' : message
        }
        return jsonify(response),200

@app.route('/train',methods=['POST'])
def train_model():
    global check_token,model
    content = request.json

    # validation
    schema = {
        'id': {'required':True},
        'token':{'required':True,'check_with':check_token},
        'answers':{'required':True,'empty':False},
        'questions':{'required':True},
        'labels':{'required':True}
    }
    validator = cerberus.Validator(schema)
    if not validator.validate(content):
        return jsonify(validator.errors),400

    th = train_handler(content['questions'],content['answers'],content['labels'],content['id'])
    model = th.train()

    return jsonify({'success':True}) , 200