import time

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SProductTemplate(models.Model):
    # Inherit from  product.template
    _inherit = 'product.template'

    date_from = fields.Date(string='Date from')
    date_to = fields.Date(string='Date to')

    product_warranty = fields.Text(string='Product Warranty', readonly=True, compute="_compute_code_warranty")
    days_left = fields.Integer(string='Remaining days of warranty', compute='_compute_date')
    status_warranty = fields.Text(string='Status Warranty', compute='_compute_warranty_left')
    product_discount = fields.Float(string='Product discount (%)', compute="_compute_product_warranty")
    active_product_discount = fields.Boolean(string="Active product discounts ", default=False, readonly=True)
    reduce_value = fields.Float(string="Value discount", readonly=True)
    # Sync Magento
    sync_magento = fields.Boolean()

    state = fields.Selection([
        ('unknown', 'Unknown'),
        ('new', 'New'),
        ('send', 'Send'),
        ('approve', 'Approve'),
        ('refuse', 'Refuse'),
    ], string='State of quotation', readonly=True, tracking=True, default='unknown')

    # Mã cũ
    ma_cu = fields.Char(string="Mã cũ")
    # Mã vật tư
    ma_vat_tu = fields.Char(string="Mã vât tư")

    # Select and Unselect Magento field
    def select_sync_magento(self):
        self.sync_magento = True

    def unselect_sync_magento(self):
        self.sync_magento = False

    def activate_product_discount_code(self):
        if self.product_discount > 0 and self.active_product_discount is False:
            self.reduce_value = self.list_price * self.product_discount / 100
            self.list_price -= self.reduce_value
            self.active_product_discount = True
        elif self.product_discount > 0 and self.active_product_discount is True:
            raise ValidationError("This product already has a discount code activated.")
        else:
            raise ValidationError("This product doesn't have any discount. Please check it out !")

    def deactivate_product_discount_code(self):
        if self.product_discount > 0 and self.active_product_discount is True:
            self.list_price += self.reduce_value
            self.reduce_value = 0
            self.active_product_discount = False
        elif self.product_discount > 0 and self.active_product_discount is False:
            raise ValidationError("This product has deactivated the discount code.")
        else:
            raise ValidationError("This product doesn't have any discount. Please check it out !")

    '''
    # Filtered để lọc các bản ghi

    @api.constrains('date_from','date_to')
    def check_available(self):
         if self.filtered(lambda r: r.date_from > r.date_to):
             raise ValidationError('Date from field must be sooner than Date to field')
    '''

    @api.constrains('date_from', 'date_to')
    def _check_available(self):
        for r in self:
            if r.date_from and r.date_to:
                if r.date_from > r.date_to:
                    raise ValidationError('[Date from] field must be sooner than [Date to] field')
            elif r.date_from != "" and r.date_to:
                raise ValidationError("Where is [Date from] ???")
            elif r.date_from and r.date_to != "":
                raise ValidationError('Where is [Date to] ???')
            else:
                pass

    @api.depends('date_from', 'date_to')
    def _compute_date(self):
        for r in self:
            r.days_left = 0
            if r.date_from and r.date_to:
                count_date = int((r.date_to - fields.Date.today()).days)
                # print(type(days_left))
                r.days_left = count_date

    # @api.onchange('product_warranty')
    # def _onchange_product_discount(self):
    #     if self.product_warranty != '':
    #         if self.days_left < 0:
    #             self.product_discount = 10
    #         else:
    #             self.product_discount = 0
    #     else:
    #         self.product_discount = 10

    @api.depends('product_warranty')
    def _compute_product_warranty(self):
        for r in self:
            if r.product_warranty != '':
                if r.days_left < 0:
                    r.product_discount = 10
                else:
                    r.product_discount = 0
            else:
                r.product_discount = 10

    # @api.depends('days_left')
    # def _compute_check_status(self):
    #     for r in self:
    #         if r.days_left == 30 or r.days_left == 31:
    #             r.status_warranty = '1 month'
    #         elif r.days_left == 60 or r.days_left == 61:
    #             r.status_warranty = '2 months'
    #         elif r.days_left == 365:
    #             r.status_warranty = '1 year'
    #         elif r.days_left == 730:
    #             r.status_warranty = '2 year'
    #         elif r.days_left <= 0:
    #             r.status_warranty = 'Out of warranty'
    #         elif r.days_left == 1:
    #             r.status_warranty = '1 day left'
    #         else:
    #             r.status_warranty = 'Still Available'

    @api.depends('date_from', 'date_to')
    def _compute_warranty_left(self):
        for r in self:
            if r.date_to and r.date_from:

                today = fields.Date.today()
                deadline_date = fields.Datetime.to_datetime(r.date_to).date()
                left_days = deadline_date - today

                years = ((left_days.total_seconds()) / (365.242 * 24 * 3600))
                years_to_int = int(years)

                months = (years - years_to_int) * 12
                months_to_int = int(months)

                days = round((months - months_to_int) * (365.242 / 12), 0)
                days_to_int = int(days)

                r.status_warranty = str(
                    years_to_int) + ' years ' + str(months_to_int) + ' months ' + str(days_to_int) + ' days '

                if r.days_left < 0:
                    r.status_warranty = 'Out of Warranty'
                else:
                    pass
            else:
                r.status_warranty = 'No warranty'

    # @api.onchange('date_from', 'date_to')
    # def _onchange_code_warranty(self):
    #     if self.date_from and self.date_to:
    #         str_from, str_to = str(self.date_from), str(self.date_to)
    #
    #         # str_day_from, str_month_from, str_year_from = \
    #         #     str(self.date_from.day), str(self.date_from.month), str(self.date_from.year)[2:]
    #         #
    #         # str_day_to, str_month_to, str_year_to =\
    #         #     str(self.date_to.day), str(self.date_to.month), str(self.date_to.year)[2:]
    #
    #         # code = 'PWD'+'/'+ str_from +'/'+ str_to
    #
    #         label_day_from = str_from[8:10] + str_from[5:7] + str_from[2:4]
    #         label_day_to = str_to[8:10] + str_to[5:7] + str_to[2:4]
    #         code = 'PWD' + '/' + label_day_from + '/' + label_day_to
    #
    #         self.product_warranty = code
    #     else:
    #         self.product_warranty = ''

    @api.depends('date_from', 'date_to')
    def _compute_code_warranty(self):

        for r in self:
            if r.date_from and r.date_to:
                str_from = str(r.date_from)
                str_to = str(r.date_to)

                # str_day_from, str_month_from, str_year_from = \
                #     str(r.date_from.day), str(r.date_from.month) + str(r.date_from.year)[2:]
                #
                # str_day_to, str_month_to, str_year_to = \
                #     str(r.date_to.day),str(r.date_to.month),str(r.date_to.year)[2:]

                label_day_from = str_from[8:10] + str_from[5:7] + str_from[2:4]
                label_day_to = str_to[8:10] + str_to[5:7] + str_to[2:4]

                code = 'PWD' + '/' + label_day_from + '/' + label_day_to
                # code2 = 'PWD'+'/' + str_from + '/' + str_to

                r.product_warranty = code
            else:
                r.product_warranty = ''
