from odoo.http import request


def success_response(message="Success", data=None, status=200):
    return request.make_json_response({
        "success": True,
        "message": message,
        "data": data or {}
    }, status=status)


def error_response(message="Error", error="", status=500):
    return request.make_json_response({
        "success": False,
        "message": message,
        "error": str(error)
    }, status=status)