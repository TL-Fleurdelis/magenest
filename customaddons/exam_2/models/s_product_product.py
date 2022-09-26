from odoo import models, fields, api


class SProductProduct(models.Model):
    _inherit = 'product.product'

    sex = fields.Char(string='Sex', compute="_compute_fashion_variants", readonly=True)
    size = fields.Char(string="Size", compute="_compute_fashion_variants", readonly=True)
    color = fields.Char(string="Color", compute="_compute_fashion_variants", readonly=True)

    @api.depends('product_template_variant_value_ids')
    def _compute_fashion_variants(self):
        for rec in self:
            rec.size = ''
            rec.sex = ''
            rec.color = ''
            if rec.product_template_variant_value_ids:
                for r in rec.product_template_variant_value_ids:
                    if r.attribute_id.display_name and r.attribute_id.display_name == 'Size':
                        rec.size = r.name
                    if r.attribute_id.display_name and r.attribute_id.display_name == 'Sex':
                        rec.sex = r.name
                    if r.attribute_id.display_name and r.attribute_id.display_name == 'Color':
                        rec.color = r.name

