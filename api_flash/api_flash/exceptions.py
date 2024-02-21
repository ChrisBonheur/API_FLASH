from rest_framework.exceptions import APIException

class CustomValidationError(APIException):
    status_code = 407
    default_detail = 'Erreur de validation.'
    default_code = 'custom_validation_error'

    def __init__(self, detail=None, code=None):
        self.status_code = code
        super().__init__(detail, code)
