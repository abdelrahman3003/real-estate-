from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Tag(models.Model):
    _name = 'tag'

    name = fields.Char(required=True)
