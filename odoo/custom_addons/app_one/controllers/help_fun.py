from odoo.http import request
def api_response(success=True, message="", data=None, status=200, error=None):
    response = {
        "success": success,
        "message": message,
    }
    if data is not None:
        response["data"] = data

    if error is not None:
        response["error"] = str(error)
    return request.make_json_response(response, status=status)