from flask import Flask, render_template, jsonify, Response, request
import cv2
import os
import numpy as np
import pandas as pd
import json
import ast 

from utils.parser import get_config

cfg = get_config()
cfg.merge_from_file('configs/services.yaml')

HOST = cfg.SERVICE.HOST
PORT = cfg.SERVICE.PORT
UPLOAD_FOLDER_TRAIN = cfg.SERVICE.UPLOAD_FOLDER_TRAIN
UPLOAD_FOLDER_TEST = cfg.SERVICE.UPLOAD_FOLDER_TEST

UPLOAD_FOLDER = None
LIST_EMOTION = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral', 'others']
# FILE_LIST = os.listdir(UPLOAD_FOLDER)

df = pd.read_csv('data/additional_infor:train_emotion_polarity.csv')
d = {'image_id': df['image_id'], 'emotion_polarity': df['emotion_polarity']}
MY_DF = pd.DataFrame(d)

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
@app.route('/home')
def view_home():
    return render_template('visual.html')

@app.route('/get_img_name')
def get_img_name():
    mode = request.args.get('mode')
    index = request.args.get('index')
    dataset = request.args.get('dataset')

    if dataset == 'train':
        UPLOAD_FOLDER = UPLOAD_FOLDER_TRAIN
    elif dataset == 'test':
        UPLOAD_FOLDER = UPLOAD_FOLDER_TEST

    FILE_LIST = os.listdir(UPLOAD_FOLDER)
    print("index: ", index)
    print("file_list[0]: ", FILE_LIST[0])
    len_file_list = len(FILE_LIST)
    fname = None
    if mode == 'path':
        for i in range(len(FILE_LIST)):
            if FILE_LIST[i] == index:
                fname = FILE_LIST[i]
                break
    else:
        index = int(index)
        if index >= len_file_list:
            fname = FILE_LIST[0]
            index = -1
        else:
            fname = FILE_LIST[index]
    
    img_id = fname.split(".")[0]
    dict_emotion = {}
    index_row = MY_DF.index[df['image_id'] == img_id].tolist()
    index_row = index_row[0]
    emotion = MY_DF['emotion_polarity'][index]
    emotion = ast.literal_eval(emotion) 
    for key_emotion in LIST_EMOTION:
        if key_emotion not in emotion:
            dict_emotion[key_emotion] = "0"
        else:
            dict_emotion[key_emotion] = str(emotion[key_emotion])
    
    # print("dict_emotion: ", dict_emotion)
    
    return_result = {'code': '1000', 'status': 'Done', \
                    'data':{'fname': fname, 'index': index, 'total': len_file_list, 'dict_emotion': dict_emotion}}

    return jsonify(return_result)

@app.route('/get_ori_img')
def get_ori_img():
    print("showed image")
    filename = request.args.get('filename')
    dataset = request.args.get('dataset')

    if dataset == 'train':
        UPLOAD_FOLDER = UPLOAD_FOLDER_TRAIN
    elif dataset == 'test':
        UPLOAD_FOLDER = UPLOAD_FOLDER_TEST

    img = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
    ret, jpeg = cv2.imencode('.jpg', img)
    return  Response((b'--frame\r\n'
                     b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tostring() + b'\r\n\r\n'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)