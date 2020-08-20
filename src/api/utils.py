def get_api_result_structure():
    result = {
        'result': True,
        'error': None,
        'data': None
    }
    return result


def set_error_result(data, msg):
    data['result'] = False
    data['error'] = msg
    return data
