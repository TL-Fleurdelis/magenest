from odoo import models, fields, api


class SProductProduct(models.Model):
    _inherit = 'product.product'

    gender = fields.Char(compute="_compute_fashion_variants", readonly=True)
    size = fields.Char(compute="_compute_fashion_variants", readonly=True)
    color = fields.Char(compute="_compute_fashion_variants", readonly=True)

    @api.depends('product_template_variant_value_ids')
    def _compute_fashion_variants(self):
        for rec in self:
            rec.size = ''
            rec.gender = ''
            rec.color = ''
            if rec.product_template_variant_value_ids:
                for r in rec.product_template_variant_value_ids:
                    if r.attribute_id.display_name and r.attribute_id.display_name == 'Size':
                        rec.size = r.name
                    if r.attribute_id.display_name and r.attribute_id.display_name == 'Gender':
                        rec.gender = r.name
                    if r.attribute_id.display_name and r.attribute_id.display_name == 'Color':
                        rec.color = r.name

