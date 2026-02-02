from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    code = 403
    message = 'User is not authorized to access'

class InputError(HTTPException):
    code = 400
    message = 'Input is invalid'
