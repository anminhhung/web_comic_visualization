from flask import Flask, render_template, jsonify, Response, request
import cv2
import os
import numpy as np
import json

from utils.parser import get_config

cfg = get_config()
cfg.merge_from_file('configs/services.yaml')

HOST = cfg.SERVICE.HOST
PORT = cfg.SERVICE.PORT
UPLOAD_FOLDER_TRAIN = cfg.SERVICE.UPLOAD_FOLDER_TRAIN
UPLOAD_FOLDER_TEST = cfg.SERVICE.UPLOAD_FOLDER_TEST

UPLOAD_FOLDER = None

app = Flask(__name__, template_folder='templates', static_folder='static')

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

    file_list = os.listdir(UPLOAD_FOLDER)
    print("index: ", index)
    print("file_list[0]: ", file_list[0])
    len_file_list = len(file_list)
    fname = None
    if mode == 'path':
        for i in range(len(file_list)):
            if file_list[i] == index:
                fname = file_list[i]
                break
    else:
        index = int(index)
        if index >= len_file_list:
            fname = file_list[0]
            index = -1
        else:
            fname = file_list[index]
    
    return_result = {'code': '1000', 'status': 'Done', 'data':{'fname': fname, 'index': index, 'total': len_file_list}}

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