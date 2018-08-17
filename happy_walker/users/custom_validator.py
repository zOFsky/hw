from cerberus import errors, Validator
import json

class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.MIN_LENGTH.code] = 'input is too short!'
    messages[errors.REGEX_MISMATCH.code] = 'incorrect format of data'

class CustomValidator(object):

    def __init__(self, validation_schema):
        self.validation_schema = validation_schema

    def request_validation(self, request):
        if len(request.body) > 0 and len(request.FILES) == 0:
            data = json.loads(request.body)

        data_validator = Validator(self.validation_schema, 
                                   error_handler=CustomErrorHandler)
        data_validator.allow_unknown = True
        # Validating password and email using cerberus library
        data_validator(data)
        errors_dict = {}
        if data_validator.errors:
            print("ERRORS: {}".format(data_validator.errors))
            errors_dict = {
                'errors': []
            }

            for key, value in data_validator.errors.items():
                for index in range(len(data_validator.document_error_tree[key].errors)):
                    errors_dict['errors'].append({
                        "field": key,
                        "code": data_validator.document_error_tree[key].errors[index].rule,
                        "message": value[index]
                    })
                    
        return errors_dict
