from odoo import fields, models, api
from odoo.exceptions import ValidationError


class TaskTimesheet(models.Model):
    _name = 'task.timesheet'

    task_id = fields.Many2one('task', required=True)
    user_id = fields.Many2one('res.users', required=True)
    date = fields.Date(default=fields.Date.today)
    hours = fields.Float(required=True)
    description = fields.Char()

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['user_id'] = self.env.user.id
        return res
    @api.model
    def create(self, vals):
        task = self.env['task'].browse(vals.get('task_id'))
        new_hours = vals.get('hours', 0)
        total = sum(task.timesheet_ids.mapped('hours'))
        if total + new_hours > task.estimated_time:
            raise ValidationError("You exceeded the estimated time of this task")
        return super().create(vals)

    def write(self, vals):
        for rec in self:
            new_hours = vals.get('hours', rec.hours)
            total = 0
            for line in rec.task_id.timesheet_ids:
                if line.id != rec.id:
                    total += line.hours
            if total + new_hours > rec.task_id.estimated_time:
                raise ValidationError("You exceeded the estimated time")
        return super().write(vals)