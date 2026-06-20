import json

from odoo import http
from odoo.http import request
from .help_fun import api_response


class PropertyApi(http.Controller):

    @http.route('/v1/property/create', methods=['POST'], type='http', auth="none", csrf=False)
    def post_property(self):
        try:
            json_vals = json.loads(request.httprequest.data.decode())
            required_fields = ['name', 'expected_price', 'description']
            for field in required_fields:
                if not json_vals.get(field):
                    return api_response(
                        success=False,
                        message="Validation Error",
                        error=f"{field} is required.",
                        status=400

                    )
            property_record = request.env['property'].sudo().create(json_vals)
            return request.make_json_response({
                "message": "Property created successfully",
                "id": property_record.id,
                "name": property_record.name,
            }, status=201)

        except Exception as error:
            return request.make_json_response({
                "message": "Something went wrong",
                "error": str(error),
            }, status=500)
        
    @http.route('/v1/property/update/<int:property_id>', methods=['PUT'], type='http', auth="none", csrf=False)
    def update_proper(self, property_id):
        property_id = request.env['property'].sudo().search([('id', '=', property_id)])
        if not property_id:
            return api_response(
                success=False,
                message="Failed to update property",
                error="Property with the given ID was not found",
                status=404
            )
        json_vals = json.loads(request.httprequest.data.decode())
        try:
            property_id.write(json_vals)
            return request.make_json_response({
                "message": "Property updated successfully",
                "id": property_id.id,
            })
        except Exception as error:
            return request.make_json_response({
                "message": "Something went wrong",
                "error": str(error),
            }, status=500)
