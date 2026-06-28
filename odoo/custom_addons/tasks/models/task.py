from odoo import fields, models, api


class Task(models.Model):
    _name = 'task'
    title = fields.Char(required=True)
    description = fields.Char(required=True)
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ], default='new')
    create_date = fields.Datetime(readonly=True)  # built-in field
    date_only = fields.Date(string="Creation Date", compute="_compute_date_only", store=False)
    developer_id = fields.Many2one('res.users', string='Developer',
    domain = lambda self: [('groups_id', 'in', self.env.ref('tasks.group_developer').id)])
    estimated_time = fields.Float()
    timesheet_ids = fields.One2many('task.timesheet', 'task_id')
    _sql_constraints = [
        ('unique_tite', 'unique(title)', 'This name already exists')
    ]
    active = fields.Boolean(default=True)
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
