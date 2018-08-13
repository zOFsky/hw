from cerberus import errors

class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.MIN_LENGTH.code] = 'input is too short!'
    messages[errors.REGEX_MISMATCH.code] = 'incorrect format of data'
