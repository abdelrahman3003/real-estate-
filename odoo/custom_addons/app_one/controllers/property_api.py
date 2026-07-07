import json
import math
from urllib.parse import parse_qs

from helper.auth_service import require_auth
from odoo import http
from odoo.http import request
from helper.api_response import success_response, error_response


class PropertyApi(http.Controller):
    @http.route('/v1/property/create', methods=['POST'], type='http', auth="public", csrf=False)
    @require_auth
    def create_property(self):
        try:
            json_vals = json.loads(request.httprequest.data.decode())
            required_fields = ['name', 'expected_price', 'description']
            for field in required_fields:
                if not json_vals.get(field):
                    return error_response(
                        message="Validation Error",
                        error=f"{field} is required",
                        status=400
                    )
            property_record = request.env['property'].sudo().create(json_vals)
            return success_response(
                message="Property created successfully",
                data={
                    "id": property_record.id,
                    "name": property_record.name
                },
                status=201
            )
        except Exception as error:
            return error_response(
                message="Something went wrong",
                error=error,
                status=500
            )

    @http.route('/v1/property/update/<int:property_id>', methods=['PUT'], type='http', auth="public", csrf=False)
    @require_auth
    def update_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().browse(property_id)
            if not property_record.exists():
                return error_response(
                    message="Property not found",
                    error="Invalid property ID",
                    status=404
                )
            json_vals = json.loads(request.httprequest.data.decode())
            property_record.write(json_vals)
            return success_response(
                message="Property updated successfully",
                data={"id": property_record.id},
                status=200
            )
        except Exception as error:
            return error_response(
                message="Something went wrong",
                error=error,
                status=500
            )

    @http.route('/v1/property/get/<int:property_id>', methods=['GET'], type='http', auth="public", csrf=False)
    @require_auth
    def get_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().browse(property_id)
            if not property_record.exists():
                return error_response(
                    message="Property not found",
                    error="Invalid property ID",
                    status=404
                )
            return success_response(
                message="Property fetched successfully",
                data={
                    "id": property_record.id,
                    "name": property_record.name or "",
                    "expected_price": property_record.expected_price or 0,
                    "description": property_record.description or "",
                    "address": property_record.address or "",
                    "phone": property_record.phone or "",
                    "state": property_record.state or "",
                },
                status=200
            )

        except Exception as error:
            return error_response(
                message="Something went wrong",
                error=error,
                status=500
            )

    @http.route('/v1/property/get_list', methods=['GET'], type='http', auth="public", csrf=False)
    @require_auth
    def get_property_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            domain = []
            page = offset = None
            limit = 0
            if params:
                if params.get('page'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])
            if page:
                offset = (page * limit) - limit
            if params.get('state'):
                domain += [('state', '=', params.get('state')[0])]
            property_records = request.env['property'].sudo().search(domain, offset=offset, limit=limit,
                                                                     order='id desc')
            property_count_ids = request.env['property'].sudo().search_count(domain)
            pagination_info = {
                "page": page,
                "limit": limit,
                "pages": math.ceil(property_count_ids / limit) if limit else 1,
                'count': property_count_ids,

            }
            data = [{
                "id": prop.id,
                "name": prop.name or "",
                "expected_price": prop.expected_price or 0,
                "description": prop.description or "",
                "address": prop.address or "",
                "phone": prop.phone or "",
                "state": prop.state or "",
            } for prop in property_records]
            return success_response(
                message="Properties fetched successfully",
                data={
                    "pagination": pagination_info,
                    "properties": data,
                },
                status=200
            )
        except Exception as error:
            return error_response(
                message="Something went wrong",
                error=error,
                status=500
            )

    @http.route('/v1/property/delete/<int:property_id>', methods=['DELETE'], type='http', auth="public", csrf=False)
    @require_auth
    def delete_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().browse(property_id)
            if not property_record.exists():
                return error_response(
                    message="Property not found",
                    error="Invalid property ID",
                    status=404
                )
            property_record.unlink()
            return success_response(
                message="Property deleted successfully",
                data={"id": property_id},
                status=200
            )
        except Exception as error:
            return error_response(
                message="Something went wrong",
                error=error,
                status=500
            )
