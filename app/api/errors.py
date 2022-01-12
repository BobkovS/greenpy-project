from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    error = 'code=' + HTTP_STATUS_CODES.get(status_code, 'Unknown error')
    if message:
        error += ' message=' + str(message)
    response = jsonify({'error': error})
    response.status_code = 200
    return response
