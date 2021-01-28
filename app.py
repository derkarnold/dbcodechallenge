import flask
import flask_restful
import waitress
import http
import logging
from analyse import TextAnalyser
_log = logging.getLogger(__name__)

# Some constants.
_DEFAULT_LISTEN_ADDRESS = '0.0.0.0'
_DEFAULT_PORT = 8000
_MAX_CONTENT_LENGTH_BYTES = 10 * 1024 * 1024 # 10MB.

# Web application.
APP = flask.Flask(__name__)
API = flask_restful.Api(APP)

@APP.route('/')
def main():
    return 'Please see <a href="/analyse">/analyse</a> endpoint.'

@API.resource('/analyse')
class AnalyseResource(flask_restful.Resource):
    def get(self):
        return 'Please POST JSON in the format of {"text":"<your text>"}'
    
    def post(self):
        request = flask.request
        if request.content_length > _MAX_CONTENT_LENGTH_BYTES:
            self.abortRequest('Content length too long: {}.'.format(request.content_length))

        reqObj = request.get_json()
        return self.processRequest(reqObj)

    def processRequest(self, request):
        if not isinstance(request, dict) or 'text' not in request:
            self.abortRequest('Invalid JSON structure. Should be a dictionary of the form {"text": "<text>"}.')

        text = request['text']
        if not isinstance(text, str):
            self.abortRequest('The text field in the request is not a valid string.')

        analyser = TextAnalyser(text)
        return self.makeResponse(analyser)
                
    def abortRequest(self, message: str, statusCode=http.HTTPStatus.BAD_REQUEST):
        _log.warn('Aborting request due to: %s', message)
        # This throws an exception.
        flask_restful.abort(statusCode.value, message=message)

    def makeResponse(self, analyser: TextAnalyser):
        '''
        Explicitly craft the response rather than relying on class object serialisation "magic".
        This is our "view" of the model.
        '''
        textLength = analyser.textLength
        return {
            'textLength': {
                'withSpaces': textLength.withSpaces,
                'withoutSpaces': textLength.withoutSpaces,
            },
            'wordCount': analyser.wordCount,
            'characterCount': analyser.characterCount,
        }

def serve(address=None, port=None):
    '''
    Start the server.
    '''
    if address is None:
        address = _DEFAULT_LISTEN_ADDRESS
    if port is None:
        port = _DEFAULT_PORT
    waitress.serve(APP, host=address, port=port)

if __name__ == '__main__':
    import os

    listenAddress = os.environ.get('LISTEN_ADDRESS', None)
    port = os.environ.get('PORT', None)
    if port is not None:
        port = int(port)
    
    serve(listenAddress, port)
