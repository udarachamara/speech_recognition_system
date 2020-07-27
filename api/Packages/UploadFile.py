import os
import secrets
from pydub import AudioSegment
from pydub.utils import make_chunks
from flask import Flask, flash, request, redirect, url_for

ALLOWED_EXTENSIONS = {'wav'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def divide_file(filename, count):
    print("Chucking started....")
    file_path = 'uploads/' + filename
    myaudio = AudioSegment.from_file(file_path, "wav")
    chunk_length_ms = 60000  # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of one sec
    # Export all of the individual chunks as wav files
    chunk_count = 0
    for i, chunk in enumerate(chunks):
        chunk_name = filename + "_chunk{0}.wav".format(i)
        chunk_count = chunk_count + 1
        print("exporting", chunk_name)
        chunk_path = 'chunk/' + chunk_name
        chunk.export(chunk_path, format="wav")

    return {'status': 'Divide done..!',
            'response_code': 1001,
            'file_name': filename,
            'chunk_count': chunk_count,
            'Application': 'Research 2020-159-speech_recognition_system',
            'version': '1.0.0'}


class UploadFile:

    @staticmethod
    def upload_file(path):
        if request.method == 'POST':
            file = request.files['file']
            f_token = secrets.token_hex(5)
            filename = f_token + '_' + file.filename
            if file and allowed_file(file.filename):
                file.save(os.path.join(path, filename))
                return {'status': 'Upload working..!',
                        'data': filename,
                        'response_code': 1001,
                        'Application': 'Research 2020-159-speech_recognition_system',
                        'version': '1.0.0'}
            else:
                return {'status': 'No file Or File Format Not Supported..!',
                        'response_code': 1002,
                        'Application': 'Research 2020-159-speech_recognition_system',
                        'version': '1.0.0'}

        else:
            return {'status': 'No Post method..!',
                    'response_code': 1003,
                    'Application': 'Research 2020-159-speech_recognition_system',
                    'version': '1.0.0'}

