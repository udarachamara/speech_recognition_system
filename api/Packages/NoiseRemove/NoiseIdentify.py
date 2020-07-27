from flask import send_file
from flask_restful import Resource


class NoiseIdentify(Resource):
    @staticmethod
    def freq_identify(key):
        return {'status': 'Request success..!',
                'response_code': 1000,
                'data': [
                    {'name': str('67382e72371.wav')},
                    {'name': str('67382e72372.wav')},
                    {'name': str('67382e72373.wav')},
                ],
                'Application': 'Research 2020-159-speech_recognition_system',
                'version': '1.0.0'}
