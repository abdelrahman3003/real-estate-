from odoo import api, fields, models


class PurchaseDashboard(models.TransientModel):
    _name = "purchase.dashboard"
    _description = "Purchase Dashboard"

    draft_count = fields.Integer(string="Draft RFQs", readonly=True)
    rfq_sent_count = fields.Integer(string="RFQs Sent", readonly=True)
    confirmed_count = fields.Integer(string="Confirmed Orders", readonly=True)
    done_count = fields.Integer(string="Done Orders", readonly=True)
    cancelled_count = fields.Integer(string="Cancelled Orders", readonly=True)
    total_purchases = fields.Integer(string="Total Purchases", readonly=True)
    monthly_purchase_amount = fields.Float(string="This Month Amount", readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        orders = self.env["purchase.order"]
        res["draft_count"] = orders.search_count([
            ("state", "=", "draft")
        ])

        res["rfq_sent_count"] = orders.search_count([
            ("state", "=", "sent")
        ])

        res["confirmed_count"] = orders.search_count([
            ("state", "=", "purchase")
        ])

        states = [value for value, _ in orders._fields["state"].selection]

        if "done" in states:
            res["done_count"] = orders.search_count([
                ("state", "=", "done")
            ])
        else:
            res["done_count"] = 0
        res["cancelled_count"] = orders.search_count([
            ("state", "=", "cancel")
        ])
        res["total_purchases"] = orders.search_count([])
        today = fields.Date.today()
        month_start = today.replace(day=1)
        monthly_orders = orders.search([
            ("date_order", ">=", month_start),
            ("state", "in", ["purchase", "done"]),
        ])
        res["monthly_purchase_amount"] = sum(
            monthly_orders.mapped("amount_total")
        )

        return res