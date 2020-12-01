from flask import Flask,request,jsonify
import json
from telebot import apihelper
import cerberus
import requests
from train_handler import train_handler
import pandas as pd
from model import MLP_model as mlp
from model import model_handle


app = Flask(__name__)
token = '1231725805:AAGNfddJG9WEEKhxgG5iSn6arrOq0m6qJ0c'
model = mlp.load_model('chatbot-model')
resource_url = ""
model_handle.load_data()

def check_token(field,value,error):
    global token
    if not value == token:
        error(field, "is not valid")


@app.route('/getChat',methods=['POST'])
def hello_world():
    global model

    content = request.json
    user_chat = {
        'update_id': content['update_id'],
        'user_id': content['message']['from']['id'],
        'first_name': content['message']['from']['first_name'],
        'last_name': content['message']['from']['last_name'],
        'username': content['message']['from']['username'],
        'text': content['message']['text'],
    }
    if model is None:
        message = "Mohon maaf, kami belum siap untuk menerima pesan"
        return apihelper.send_message(token, content['message']['chat']['id'], message)
    else:
        message = model_handle.get_answer(model,user_chat['text'])
        return apihelper.send_message(token, content['message']['chat']['id'], message)

@app.route('/train',methods=['POST'])
def train_model():
    global check_token,model
    content = request.json
    schema = {
        'id': {'required':True},
        'token':{'required':True,'check_with':check_token},
        'answers':{'required':True},
        'questions':{'required':True},
        'labels':{'required':True}
    }
    validator = cerberus.Validator(schema)
    if not validator:
        return jsonify(validator.errors),400
    th = train_handler(content['questions'],content['answers'],content['labels'])
    model = th.train()
    model_handle.load_data()
    return jsonify({'success':True}) , 200