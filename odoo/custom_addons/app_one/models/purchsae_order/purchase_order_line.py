from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.constrains('product_qty')
    def _check_quantity(self):
        for rec in self:
            if rec.product_qty <= 0:
                raise ValidationError("Quantity must be greater than 0")
