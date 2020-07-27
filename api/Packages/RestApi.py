from flask_restful import Resource


class RestApi(Resource):
    def get(self):
        return {'status': 'Server working..!',
                'response_code': 200,
                'Application': 'Research 2020-159-speech_recognition_system',
                'version': '1.0.0'}
