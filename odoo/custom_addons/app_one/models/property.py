from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True,translate=True)
    ref = fields.Char(default='New', readonly=True)
    address = fields.Char()
    phone = fields.Char()
    description = fields.Text(translate=True)
    postcode = fields.Char()
    date_availability = fields.Date(tracking=True)
    create_time = fields.Datetime(default=fields.datetime.now())
    expected_selling_date = fields.Date(tracking=True)
    is_late = fields.Boolean(readonly=True)
    expected_price = fields.Float(required=True, digits=(6, 4))
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff_price', store=True)
    bedrooms = fields.Integer()
    leaves = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Boolean()
    garden_operator = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft')
    owner_id = fields.Many2one("owner")
    tag_ids = fields.Many2many("tag")
    bedrooms_ids = fields.One2many("bedroom", 'property_id')
    owner_address = fields.Char(related='owner_id.address')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'This name already exists')
    ]

    @api.constrains('expected_price')
    def _check_price(self):
        for rec in self:
            if rec.expected_price <= 0:
                raise ValidationError('Price cannot be zero')

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft','')
            rec.state = 'draft'

    def action(self):
        print(self.env['property'].search([('name', '!=', 'property 1')]))

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending','')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold','')
            rec.state = 'sold'
            print(rec.state)

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed', '')
            rec.state = 'closed'
            print(rec.state)

    @api.depends('expected_price', 'selling_price')
    def _compute_diff_price(self):
        for rec in self:
            print(" _compute_diff_price depends")
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price', 'selling_price')
    def _onchange_expected_price(self):
        for rec in self:
            if (rec.expected_price - rec.selling_price) < 0:
                return {
                    'warning': {'title': 'warning', 'message': "negative value", 'type': 'notification'}
                }

    def check_expected_selling_date(self):
        print("check_expected_selling_date")
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def create_history_record(self, old_state, new_state, reason):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area}) for line in rec.bedrooms_ids],
            })

    def action_open_change_state(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {"default_property_id": self.id}
        return action

    def action_open_related_owner(self):
        action=self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form')
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id.id, 'form']]
        return action


class Bedroom(models.Model):
    _name = 'bedroom'
    area = fields.Integer()
    description = fields.Char()
    property_id = fields.Many2one('property')

    # @api.model_create_multi
    # def create(self,vals):
    #     res = super(Property, self)._create(vals)
    #     print("inside create method")
    #     return res
    # def write(self,vals):
    #     res = super(Property, self)._write(vals)
    #     print("inside write method")
    #     return res
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("inside unlink method")
    #     return res
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None):
    #     res = super(Property, self)._search(domain, offset, limit, order)
    #     print("inside search method")
    #     return res
