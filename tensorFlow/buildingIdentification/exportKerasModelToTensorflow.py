import keras.backend as K
import tensorflow as tf
from keras.models import load_model, Sequential
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

fileName = "kerasModel_20180312-083230" #120,000 images in training + 10,600 notBuilding Idaho examples

modelPath =  r"C:\\Google Drive\\code\\python_code\\tensorFlow\\buildingIdentification\\results\\" + fileName
exportPath = r"C:\\Google Drive\\code\python_code\\tensorFlow\\buildingIdentification\\results\\kerasModel_exportToGCP" + fileName

# reset session
K.clear_session()
sess = tf.Session()
K.set_session(sess)

# disable loading of learning nodes
K.set_learning_phase(0)

# load model
model = load_model(modelPath)
config = model.get_config()
weights = model.get_weights()
new_Model = Sequential.from_config(config)
new_Model.set_weights(weights)

# export saved model
export_path = 'YOUR_EXPORT_PATH' + '/export'
builder = saved_model_builder.SavedModelBuilder(export_path)

signature = predict_signature_def(inputs={'INPUT': new_Model.input},
                                  outputs={'OUTPUT': new_Model.output})

with K.get_session() as sess:
    builder.add_meta_graph_and_variables(sess=sess,
                                         tags=[tag_constants.SERVING],
                                         signature_def_map={
                                             signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: signature})
    builder.save()   
