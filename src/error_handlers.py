import logging

from flask import Response, json

from src.api.utils import get_api_result_structure, set_error_result

logger = logging.getLogger(__name__)


def handle_api_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    logger.info('Api Exception', e.msg)

    data = get_api_result_structure()
    set_error_result(data, msg=e.msg)
    return Response(json.dumps(data), content_type='application/json')


def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    logger.info('Http Exception', e.description)

    response = e.get_response()
    data = get_api_result_structure()
    set_error_result(data, msg=e.description)
    # replace the body with JSON
    response.data = json.dumps(data)
    response.content_type = "application/json"
    return response


def handle_server_exception(e):
    data = get_api_result_structure()

    msg = 'Server Error'
    logger.exception(msg)

    set_error_result(data, msg=msg)
    return Response(json.dumps(data), status=500, content_type='application/json')

