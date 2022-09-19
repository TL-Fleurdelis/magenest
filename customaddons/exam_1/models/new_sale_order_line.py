from odoo import models, fields, api


class NewSaleOderLine(models.Model):
    _inherit = 'sale.order.line'

    code_value_line = fields.Float(related='order_id.code_value')
    
    @api.depends('product_uom_qty', 'discount', 'code_value_line', 'tax_id')
    def _compute_amount(self):
        for line in self:
            # price = line.code_value_line * (1 - (line.discount or 0.0) / 100.0)
            price = line.price_unit - (line.code_value_line * line.price_unit / 100)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                    'account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
