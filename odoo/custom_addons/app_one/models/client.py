from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Client(models.Model):
    _name = 'client'
    _inherit = 'owner'





