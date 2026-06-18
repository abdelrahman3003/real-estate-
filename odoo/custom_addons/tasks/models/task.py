from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Task(models.Model):
    _name = 'task'
    title = fields.Char(required=True)
    description = fields.Char(required=True)
    status = fields.Selection([
        ('new', 'New' ),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ],default='new')
    create_date = fields.Datetime(readonly=True)  # built-in field
    date_only = fields.Date(string="Creation Date", compute="_compute_date_only", store=False)
    assign_to = fields.Many2one("res.partner")

    @api.depends('create_date')
    def _compute_date_only(self):
        for rec in self:
            rec.date_only = rec.create_date.date() if rec.create_date else False






