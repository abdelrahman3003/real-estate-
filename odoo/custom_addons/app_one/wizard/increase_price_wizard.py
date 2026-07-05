from odoo import fields, models
from odoo.exceptions import ValidationError, UserError


class IncreasePriceWizard(models.TransientModel):
    _name = "increase.price.wizard"
    _description = "increase price product"
    percentage = fields.Float(string="Percentage")

    def action_confirm(self):
        if self.percentage <= 0:
            raise ValidationError("Percentage must be greater than zero.")
        purchase_order = self.env["purchase.order"].browse(
            self.env.context.get("active_id")

        )
        for line in purchase_order.order_line:
            line.price_unit += line.price_unit * (self.percentage / 100)

        return {"type": "ir.actions.act_window_close"}