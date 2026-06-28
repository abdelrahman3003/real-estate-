from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    expected_delivery_notes = fields.Text(
        string="Expected Delivery Notes"
    )
    purchase_priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'medium'),
        ('high', 'High'),
    ], string="Priority",
        default='medium')
