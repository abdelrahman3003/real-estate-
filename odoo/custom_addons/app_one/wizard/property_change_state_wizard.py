from odoo import fields, models
from odoo.exceptions import ValidationError, UserError


class ChangeState(models.TransientModel):
    _name = "change.state"
    _description = "Change State"
    property_id = fields.Many2one('property')
    state = fields.Selection([
        ("draft", "Draft"),
        ("pending", "Pending"),
    ], default="draft")
    reason = fields.Char(required=True)

    def action_confirm(self):
        if self.property_id.state != "closed":
            raise UserError("You can only change state when property is Closed")
        self.property_id.state = self.state
        self.property_id.create_history_record("closed",self.state,self.reason)