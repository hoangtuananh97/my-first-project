from _datetime import datetime

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if isinstance(exc, PageNotFound):
        response.data = None
        return response

    if response is not None:
        code = exc.default_code
        message = exc.detail
        response.data = {
            'status': "ERROR",
            'body': None,
            'error': {
                'message': message,
                'code': code,
                'timestamp': datetime.now(),
            }
        }
        response.content_type = 'application/json'

    return response


class PageNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found.'
    default_code = 'not_found'


class BadRequestException(APIException):
    status_code = 400
    default_detail = 'Bad request'
