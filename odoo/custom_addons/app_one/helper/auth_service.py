from functools import wraps

from helper.api_response import error_response
from odoo.http import request


def get_user_from_token():
    token = request.httprequest.headers.get('Authorization')
    if not token:
        return None
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    user = request.env['res.users'].sudo().search([
        ('api_token', '=', token)
    ], limit=1)
    return user


def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_user_from_token()
        if not user:
            return error_response(
                message="Unauthorized",
                error="Invalid or missing token",
                status=401
            )
        request.current_user = user
        return func(*args, **kwargs)

    return wrapper
