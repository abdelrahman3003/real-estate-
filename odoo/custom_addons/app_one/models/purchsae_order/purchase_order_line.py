from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.constrains('product_qty')
    def _check_quantity(self):
        for rec in self:
            if rec.product_qty <= 0:
                raise ValidationError("Quantity must be greater than 0")
    def write(self, vals):
        restricted_fields = {"product_id", "product_qty", "price_unit"}
        for line in self:
            if line.order_id.state == "done" and restricted_fields.intersection(vals):
                raise ValidationError(
                    "You cannot modify product, quantity or unit price when the purchase order is done."
                )
        return super().write(vals)
