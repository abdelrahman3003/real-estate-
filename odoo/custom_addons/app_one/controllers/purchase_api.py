import json
import math
from urllib.parse import parse_qs

from helper.api_response import success_response, error_response
from helper.auth_service import require_auth
from odoo import http
from odoo.http import request


class PurchaseApi(http.Controller):

    @staticmethod
    def _get_pagination(params):
        page = int(params.get("page", [1])[0])
        limit = int(params.get("limit", [10])[0])
        offset = (page - 1) * limit
        return page, limit, offset

    @staticmethod
    def _pagination_response(page, limit, total_count):
        return {
            "page": page,
            "limit": limit,
            "pages": math.ceil(total_count / limit) if limit else 1,
            "count": total_count,
        }

    @http.route("/v1/purchases/get_list", methods=["GET"], type="http", auth="public", csrf=False, )
    @require_auth
    def get_purchase_list(self, **kwargs):
        try:
            params = parse_qs(request.httprequest.query_string.decode())
            page, limit, offset = self._get_pagination(params)
            domain = []
            if params.get("state"):
                domain.append(("state", "=", params.get("state")[0]))
            purchase_model = request.env["purchase.order"].sudo()
            purchase_orders = purchase_model.search(
                domain,
                offset=offset,
                limit=limit,
                order="id desc",
            )

            total_count = purchase_model.search_count(domain)

            data = [
                {
                    "id": purchase.id,
                    "name": purchase.name,
                    "vendor": purchase.partner_id.name,
                    "state": purchase.state,
                    "priority": purchase.purchase_priority,
                    "reference": purchase.partner_ref or "",
                    "total_quantity": purchase.total_quantity,
                    "amount_total": purchase.amount_total,
                }
                for purchase in purchase_orders
            ]

            return success_response(
                message="Purchase orders fetched successfully",
                data={
                    "pagination": self._pagination_response(
                        page,
                        limit,
                        total_count,
                    ),
                    "purchase_orders": data,
                },
                status=200,
            )

        except Exception as error:
            return error_response(
                message="Something went wrong",
                error=error,
                status=500,
            )

    @http.route('/v1/purchases/create', methods=['POST'], type='http', auth="public", csrf=False)
    @require_auth
    def create_purchase(self, **kwargs):
        try:
            body = json.loads(request.httprequest.data or "{}")
            purchase = request.env["purchase.order"].sudo().create({
                "partner_id": body.get("partner_id"),
                "purchase_priority": body.get("purchase_priority"),
                "expected_delivery_notes": body.get("expected_delivery_notes"),
                "order_line": [
                    (0, 0, {
                        "product_id": body.get("product_id"),
                        "product_qty": body.get("quantity"),
                        "price_unit": body.get("price_unit"),
                    })
                ],
            })
            return success_response(
                message="Purchase order created successfully",
                data={
                    "id": purchase.id,
                    "name": purchase.name,
                },
                status=201,
            )
        except Exception as error:
            return error_response(
                message="Something went wrong",
                error=error,
                status=500,

            )

    @http.route("/v1/purchases/delete/<int:purchase_id>", methods=["DELETE"], type="http", auth="public", csrf=False)
    @require_auth
    def delete_purchase(self, purchase_id, **kwargs):
        try:
            purchase = request.env["purchase.order"].sudo().browse(purchase_id)
            if not purchase.exists():
                return error_response(
                    message="Purchase order not found",
                    status=404,
                )
            purchase.unlink()
            return success_response(
                message="Purchase order deleted successfully",
                status=200,
            )

        except Exception as error:
            return error_response(
                message="Something went wrong",
                error=error,
                status=500,
            )
