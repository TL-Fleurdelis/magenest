from odoo import models, fields, api


class ProductTemplateAddWarrantyWizard(models.Model):
    _name = 'product.template.add.warranty.wizard'
    _description = 'Product Template Add Warranty Wizard'

    product_id = fields.Many2many('product.template', string='Product')
    wiz_date_from = fields.Date()
    wiz_date_to = fields.Date()
    wiz_product_warranty = fields.Text()

    @api.onchange('wiz_date_from', 'wiz_date_to')
    def _onchange_code_warranty(self):
        if self.wiz_date_from and self.wiz_date_to:
            str_from, str_to = str(self.wiz_date_from), str(self.wiz_date_to)

            # str_day_from, str_month_from, str_year_from = \
            #     str(self.wiz_date_from.day), str(self.wiz_date_from.month), str(self.wiz_date_from.year)[2:]
            #
            # str_day_to, str_month_to, str_year_to =\
            #     str(self.wiz_date_to.day), str(self.wiz_date_to.month), str(self.wiz_date_to.year)[2:]

            # code = 'PWD'+'/'+ str_from +'/'+ str_to

            label_day_from = str_from[8:10] + str_from[5:7] + str_from[2:4]
            label_day_to = str_to[8:10] + str_to[5:7] + str_to[2:4]
            code = 'PWD' + '/' + label_day_from + '/' + label_day_to

            self.wiz_product_warranty = code
        else:
            self.wiz_product_warranty = ''

    def set_warranty_for_product(self):
        self.product_id.write({

            'date_from': self.wiz_date_from,
            'date_to': self.wiz_date_to,
            'product_warranty': self.wiz_product_warranty,
        })
