from odoo.tests.common import TransactionCase
from odoo import  fields


class TestProperty(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()
        self.property_01_record=self.env['property'].create({
            'ref':'PRT00012',
            'name':'Property 01',
            'description':'Property description',
            'postcode':'1234345',
            'date_availability':fields.Date.today(),
            'expected_price':12000
        })
    def test_01_property_values(self):
        property_id=self.property_01_record
        self.assertRecordValues(property_id,[{
         'ref': 'PRT00012',
         'name': 'Property 01',
         'description': 'Property description',
         'postcode': '1234345',
         'date_availability': fields.Date.today(),
         'expected_price': 12000
     }])
