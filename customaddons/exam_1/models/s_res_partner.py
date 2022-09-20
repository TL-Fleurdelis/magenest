from odoo import models, fields, api


class SResPartner(models.Model):
    _inherit = 'res.partner'

    customer_discount_code = fields.Text(string='Customer discount code', store=True)
    active_discount_code = fields.Boolean(string='Active Discount', required=False, default=False)
    code_value = fields.Float(string="Code value (%)", compute='_compute_code_value')

    # Insert value of Discount Code to print Discount Code
    @api.depends('active_discount_code', 'customer_discount_code')
    def _compute_customer_discount_code(self):
        code = 'VIP_'
        for r in self:
            if r.active_discount_code is True:
                r.customer_discount_code = code + str(r.code_value)
            else:
                r.customer_discount_code = ''

    # Process the discount code string and get the value of the code
    @api.depends('active_discount_code', 'customer_discount_code')
    def _compute_code_value(self):
        for r in self:

            r.code_value = 0
            r.active_discount_code = False

            if r.customer_discount_code != '':

                take_code_value = str(r.customer_discount_code).split('_')
                show_code_value = take_code_value[-1]

                if take_code_value[0] == 'VIP':
                    if 0 < int(show_code_value) < 100:
                        r.active_discount_code = True
                        r.code_value = int(show_code_value)
                    else:
                        r.active_discount_code = True
                        r.code_value = 100
