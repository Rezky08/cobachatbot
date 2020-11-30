from train_handler import train_handler
import json
import numpy as np
with open('./params.json','r') as param:
    params = json.load(param)

th = train_handler(params['questions'],params['answers'],params['labels'])
model = th.train()
text_tokenized = th.prep_text(params['questions'][0]['question_text'])
to_input = np.array([th.to_input(text_tokenized)])
res = model.predict(to_input)[0]
th.predict(model,params['questions'][0]['question_text'])
