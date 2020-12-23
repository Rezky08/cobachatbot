import tensorflow as tf
import filepath
from datetime import datetime
import re,os
cur_date = datetime.today()
model_location = filepath.path('/model')
model_name = "save-model-{}".format(cur_date.strftime("%Y%m%d"))
save_location = "{}/{}".format(model_location,model_name)
def create_model(x_input,hidden_layer,y_output):
    layers = [
        tf.keras.layers.Input(shape=x_input.shape)
    ]
    # add hidden layers
    for hl in hidden_layer:
        try:
            layers.append(tf.keras.layers.Dense(hl[0],activation=hl[1] if hl[1] else 'relu'))
        except:
            layers.append(tf.keras.layers.Dense(hl, activation='relu'))
    layers.append(tf.keras.layers.Dense(len(y_output),activation='softmax'))
    model = tf.keras.models.Sequential(layers)
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer='adam',
                  loss=loss_fn,
                  metrics=['accuracy'])
    return model
def train_model(model,x_train,y_train,x_test,y_test,epoch=100,early_stop=False):
    callback = tf.keras.callbacks.EarlyStopping(monitor='loss',patience=50)
    model.fit(x_train, y_train, epochs=epoch,callbacks=[callback])
    model.evaluate(x_test,y_test , verbose=2)
    return model
def save_model(model,name=None):
    model.save("{}/{}".format(model_location,model_name if name == None else name))

def load_model(path=None):
    global save_location,model_location
    list_dir = os.listdir(model_location)
    filename_re = "{}".format("save-model-{1,}" if path == None else path)
    pattern = re.compile(filename_re)
    model_exists = ""
    for filename in list_dir:
        if pattern.match(filename):
            model_exists = filename
            break
    model = None
    try:
        model = tf.keras.models.load_model("{}/{}".format(model_location,model_exists))
    except:
        pass
    return model
