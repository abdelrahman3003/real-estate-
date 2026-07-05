from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    _APPROVAL_LIMIT = 10000
    _UNPAID_BILLS_LIMIT = 50
    _UNPAID_AMOUNT_LIMIT = 100000

    expected_delivery_notes = fields.Text(
        string="Expected Delivery Notes"
    )

    purchase_priority = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        string="Purchase Priority",
        default="medium",
    )

    total_quantity = fields.Float(
        compute="_compute_total_quantity",
        store=True,
    )

    line_count = fields.Integer(
        compute="_compute_line_count",
    )

    def button_confirm(self):
        self._check_order_lines()
        self._check_vendor_credit()
        return self._confirm_or_request_approval()

    def approve(self):
        self.write({"state": "purchase"})
        return super().button_confirm()

    def _check_order_lines(self):
        for order in self:
            if not order.order_line:
                raise ValidationError(
                    "You cannot confirm an order without order lines."
                )

    def _check_vendor_credit(self):
        account_move = self.env["account.move"]

        for order in self:
            unpaid_bills = account_move.search([
                ("partner_id", "=", order.partner_id.id),
                ("move_type", "=", "in_invoice"),
                ("state", "=", "posted"),
                ("payment_state", "!=", "paid"),
            ])

            if len(unpaid_bills) > self._UNPAID_BILLS_LIMIT:
                raise ValidationError(
                    "Cannot confirm this purchase order because the vendor has more than 50 unpaid vendor bills."
                )

            total_unpaid = sum(unpaid_bills.mapped("amount_residual"))

            if total_unpaid > self._UNPAID_AMOUNT_LIMIT:
                raise ValidationError(
                    "Cannot confirm this purchase order because the vendor's unpaid balance exceeds the allowed limit."
                )

    def _confirm_or_request_approval(self):
        for order in self:
            if order.amount_total > self._APPROVAL_LIMIT:
                order.state = "to approve"
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "title": "Approval Required",
                        "message": "This purchase order has been submitted for manager approval.",
                        "type": "warning",
                        "sticky": False,
                    },
                }

        return super().button_confirm()

    @api.depends("order_line.product_qty")
    def _compute_total_quantity(self):
        for order in self:
            order.total_quantity = sum(order.order_line.mapped("product_qty"))

    @api.depends("order_line")
    def _compute_line_count(self):
        for order in self:
            order.line_count = len(order.order_line)

    def open_view_order_lines(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Order Lines",
            "res_model": "purchase.order.line",
            "view_mode": "tree,form",
            "domain": [("order_id", "=", self.id)],
            "context": {
                "default_order_id": self.id,
            },
        }

    def duplicate_purchase_order(self):
        self.ensure_one()

        new_purchase = self.copy(
            default={
                "partner_ref": False,
                "state": "draft",
            }
        )

        new_purchase.message_post(
            body="Purchase duplicated successfully."
        )

        return {
            "type": "ir.actions.act_window",
            "name": "Purchase Order",
            "res_model": "purchase.order",
            "view_mode": "form",
            "res_id": new_purchase.id,
            "target": "current",
        }

    def action_done(self):
        self.write({"state": "done"})

    @api.constrains("order_line")
    def _check_duplicate_products(self):
        for order in self:
            products =set()
            for line in order.order_line:
                if line.product_id.id in products:
                    raise ValidationError(
                        "You cannot add the same product more than once in a purchase order."
                    )
                products.add(line.product_id.id)