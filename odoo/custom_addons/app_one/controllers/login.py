import uuid

from helper.api_response import error_response, success_response
from odoo import http
from odoo.http import request


class AuthController(http.Controller):

    @http.route('/v1/login', auth='public', type='http', methods=['POST'], csrf=False)
    def login(self, **kwargs):

        login = request.params.get('login')
        password = request.params.get('password')

        if not login or not password:
            return error_response(
                message="Invalid credentials",
                error="login or password is required",
                status=400
            )

        try:
            try:
                uid = request.session.authenticate(
                    request.db,
                    login,
                    password
                )
            except Exception:
                return error_response(
                    message="Invalid credentials",
                    error="login or password is not correct",
                    status=401
                )

            if not uid:
                return error_response(
                    message="Invalid credentials",
                    error="login or password is not correct",
                    status=401
                )

            user = request.env['res.users'].sudo().browse(uid)

            if not user.api_token:
                user.api_token = str(uuid.uuid4())

            return success_response(
                message="Login success",
                data={
                    "token": user.api_token
                },
                status=200
            )

        except Exception as e:
            return error_response(
                message="Something went wrong",
                error=str(e),
                status=500
            )