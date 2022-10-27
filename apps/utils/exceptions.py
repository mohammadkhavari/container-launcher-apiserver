from rest_framework.exceptions import APIException
from rest_framework import status


class ImageNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'App image is not available'
    default_code = 'bad_request'

class DockerAPIError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "An error occurred on calling docker API client"
    defualt_code = "internal_server_error"