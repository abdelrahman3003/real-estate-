from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    expected_delivery_notes = fields.Text(
        string="Expected Delivery Notes"
    )
    purchase_priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'medium'),
        ('high', 'High'),
    ], string="purchase priority",
        default='medium')
    total_quantity = fields.Float(
        compute="_compute_total_quantity",
        store=True
    )
    line_count = fields.Integer(
        compute="_compute_line_count"
    )

    def button_confirm(self):
        for order in self:
            if not order.order_line:
                raise ValidationError("You cannot confirm an order without order lines.")
        return super().button_confirm()

    @api.depends('order_line.product_qty')
    def _compute_total_quantity(self):
        for order in self:
            order.total_quantity = sum(order.order_line.mapped('product_qty'))

    def action(self):
        print("0000000")

    @api.depends("order_line")
    def _compute_line_count(self):
        for order in self:
            order.line_count = len(order.order_line)
    def action_view_order_lines(self):
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

