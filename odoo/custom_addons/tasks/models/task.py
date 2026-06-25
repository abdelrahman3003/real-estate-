from email.policy import default

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
        ('closed', 'Closed'),
    ],default='new')
    create_date = fields.Datetime(readonly=True)  # built-in field
    date_only = fields.Date(string="Creation Date", compute="_compute_date_only", store=False)
    assign_to = fields.Many2one("res.partner")
    active=fields.Boolean(default=True)
    deadline = fields.Date()
    is_late = fields.Boolean(default=False)

    @api.depends('create_date')
    def _compute_date_only(self):
        for rec in self:
            rec.date_only = rec.create_date.date() if rec.create_date else False

    def action_closed(self):
        for rec in self:
            rec.status = 'closed'

    def check_task_deadline_date(self):
        task_ids = self.search([])
        for rec in task_ids:
            if rec.deadline and rec.deadline < fields.Date.today():
                rec.is_late = True











