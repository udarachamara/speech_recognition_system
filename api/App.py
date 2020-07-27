"""
@Author
I M U C Herath
IT16113732

@createAt
2020-03-24 10:00:00 am

This is main class for handle api request

"""
import base64
import os
import threading
import time

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Api
from Packages.RestApi import RestApi
from Packages.UploadFile import UploadFile
from Packages.NoiseRemove.Identity import Identity

from Packages.NoiseRemove.NoiseIdentify import NoiseIdentify

from Packages.ConvertUnicode.ConUniText import ConUniText

from Packages.BackgroundEffect.BackgroundEffect import BackgroundEffect

from Packages.UploadFile import divide_file

UPLOAD_FOLDER = 'uploads'
OUT_FOLDER = 'out'
app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api.add_resource(RestApi, '/api')  # Route_Default

tmp_file_name = ""


@app.route('/api/uploadFile', methods=['GET', 'POST'])
def upload_file():
    res = UploadFile.upload_file(app.config['UPLOAD_FOLDER'])
    if res['response_code'] == 1001:
        app.tmp_file_name = res['data']
        # return res
        # return Identity.noise_identity_and_remove(res['data'])
        res1 = divide_file(res['data'], 2)
        return res1
    else:
        return res


@app.route('/api/getProcessFreqFiles/<path:key>', methods=['GET'])
def get_freq_file_all(key):
    res = NoiseIdentify.freq_identify(key)
    return res


@app.route('/api/convertText', methods=['GET'])
def convert_file_to_text():
    res = ConUniText.convert_to_text(app.tmp_file_name)
    return res


@app.route('/api/removeBackgroundEffect/<path:out_name>', methods=['GET'])
def remove_background_effects(out_name):
    index = 0

    for j in range(2):
        print("J =>", j)
        thread1 = threading.Thread(target=test, args=(out_name, index))
        thread1.daemon = True
        thread1.start()
        index = index + 1

    return {'status': 'Thread working..!',
            'data': out_name,
            'response_code': 1000,
            'Application': 'Research 2020-159-speech_recognition_system',
            'version': '1.0.0'}


def test(out_name, index):
    res = BackgroundEffect.split_vocal(out_name, index)
    time.sleep(2)


@app.route('/api/getProcessFreqFilesByName/<path:filename>', methods=['GET'])
def get_freq_file(filename):
    # res = NoiseIdentify.freq_identify()
    # return res
    print(filename)
    path = 'out/' + filename
    # file = send_from_directory('out', filename)
    with open(path, "rb") as ad_file:
        encoded_string = base64.b64encode(ad_file.read())
        encoded_string = encoded_string
    return {'base64': str(encoded_string)}


if __name__ == '__main__':
    app.run(port='5002')
