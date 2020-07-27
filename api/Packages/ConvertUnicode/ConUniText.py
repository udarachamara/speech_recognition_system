import speech_recognition as sr
import time
from flask_restful import Resource


class ConUniText(Resource):
    @staticmethod
    def convert_to_text(filename):
        if filename != "":
            start = time.time()
            r = sr.Recognizer()
            file_path = 'uploads/' + filename
            print(file_path)
            rec = sr.AudioFile(file_path)

            with rec as source:
                audio = r.record(source)

            text = r.recognize_google(audio, language='si-LK')
            print(text)

            print("response time in seconds")
            print(time.time() - start)
            return {'status': 'Request Success..!',
                    'uni_text': str(text),
                    'response_code': 1000,
                    'Application': 'Research 2020-159-speech_recognition_system',
                    'version': '1.0.0'}

        else:
            return {'status': 'Request Failed..!',
                    'response_code': 1005,
                    'Application': 'Research 2020-159-speech_recognition_system',
                    'version': '1.0.0'}



