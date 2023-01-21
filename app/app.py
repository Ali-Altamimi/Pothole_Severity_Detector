import base64
import flask
from pathlib import Path
import os
import time
import base64
from io import BytesIO
from PIL import Image
import os
from pymongo import MongoClient
import  time
import torch
import pandas as pd
from datetime import datetime
from bson.objectid import ObjectId
from flask import Flask, render_template, Response
from camera import VideoCamera, model
import cv2



client = MongoClient('mongodb+srv://0xc4d:123@cluster0.qaindan.mongodb.net/?retryWrites=true&w=majority')

db = client['pothole']

app = flask.Flask(__name__)
app_root = os.path.dirname(os.path.abspath(__file__))



UPLOAD_FOLDER = f'{app_root}\static\img\\'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def login():
    return flask.render_template('index.html')


@app.route('/camera')
def home():
    return flask.render_template('camera.html')

@app.route('/api/saveImage', methods=['POST'])
def save_image():
    os.chdir(UPLOAD_FOLDER)
    print(os.getcwd())
    print(flask.request.get_data())
    desc = flask.request.args.get('description')
    print(desc)
    if 'files' not in flask.request.files:
        return flask.jsonify({'status': 'false', 'message': 'No file part', 'url': flask.request.url})
    file = flask.request.files['files']
    if file.filename == '':
        return flask.jsonify({'status': 'false', 'message': 'No image selected for uploading', 'url': flask.request.url})
    if file and allowed_file(file.filename):
        timeNow = time.time()
        destination = f'img\{timeNow}{file.filename}'
        print(timeNow)
        file.save(destination)
        os.chdir(app_root)
        #print(os.popen(f"python yolov5/detect.py --weights yolov5/best.pt --source static/img/{destination}").read())

        severity_type = yolo(destination)
        delImg = destination.replace('img\\', '').replace('.png', '').replace('.jpg', '')

        db['severity-potholes'].insert_one({'description': desc,
                                            'imgPath': '../static/img/'+destination,
                                            'imgResult': f'../static/img/results/{delImg}.jpg',
                                            'time': time.time(),
                                            'severity_type': severity_type,
                                            'currentDate': datetime.now(),
                                            'category': 'upload-image'
                                            })
        print(True)

        return flask.jsonify({'status': 'true', 'message': 'Save images successfully', 'url': flask.request.url, 'path': f'../static/img/results/{delImg}.jpg'})
    else:
        return flask.jsonify({'status': 'false', 'message': 'Allowed image types are -> png, jpg, jpeg, gif', 'url': flask.request.url})

@app.route('/api/camera', methods=['POST'])
def test():

    # data = flask.request.get_json()

    # lang = flask.request.args.get('lang')
    # lat = flask.request.args.get('lat')


    # if data is None:
    #     print("No valid request body, json missing!")
    #     return flask.jsonify({'status': 'false', 'error': 'No valid request body, json missing!'})
    # else:
    #     img_data = data['img']
    #     original_img = convert_and_save(img_data)

    #     severity_type = yolo(original_img)
    #     delImg = original_img.replace('img\\', '').replace('.png', '')

    #     db['severity-potholes'].insert_one({'imgPath': original_img,
    #                                     'imgResult': f'../static/img/results/{delImg}.jpg',
    #                                     'time': time.time(),
    #                                     'severity_type': severity_type,
    #                                     'currentDate': datetime.now(),
    #                                     'category': 'camera'
    #                                     })
    #     return flask.jsonify({'status': 'true', 'message': 'Save images successfully', 'url': flask.request.url})
    pass

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def convert_and_save(file):
    starter = file.find(',')
    image_data = file[starter+1:]
    image_data = bytes(image_data, encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data)))
    img = f'static/img/camera/{time.time()}.png'
    im.save(img)
    return img



@app.route('/upload-img')
def upload_image():
    return flask.render_template('uploading.html')

@app.route('/list')
def lists():
    find_all = db['severity-potholes'].find({})
    arr = []
    for item in find_all:
        print(item['_id'])
        arr.append(item)
    return flask.render_template('lists.html', potholes = arr)  

def yolo(path):
    img = path
    image_full_path = f'static\\img\\{img}'
    results = model(image_full_path)
    
    results.save(save_dir=f'static\\img\\results', exist_ok=True)
    results.print()


    x = results.pandas().xyxy[0]
    max_value = x['class'].max()
    print(x)
    if(max_value > -1):
        return x[x['class'] == max_value]['name'].values[0]
    return 'There is no result'


@app.route('/api/update-status', methods=['POST'])
def update_status():
    docId = flask.request.args.get('id')
    bool = flask.request.args.get('bool')
    # print(docId, bool)
    getDocById = db['severity-potholes'].find_one({"_id": ObjectId(docId)})
    # print(getDocById)
    # print(getDocById['_id'], docId)
    # print(str(ObjectId(getDocById['_id'])) == docId)
    if str(ObjectId(getDocById['_id'])) == docId:
        getDocById['isAccurate'] = bool
        print(getDocById)
        db['severity-potholes'].update_one({'_id':ObjectId(docId)}, {"$set": getDocById}, upsert=False)
        return flask.jsonify({'status': 'true', 'message': 'Status is updated', 'url': flask.request.url})
    return flask.jsonify({'status': 'false', 'message': 'Status is fail id not found', 'url': flask.request.url})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)