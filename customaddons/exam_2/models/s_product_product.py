from odoo import models, fields, api


class SProductProduct(models.Model):
    _inherit = 'product.product'

    gender = fields.Char(compute="_compute_fashion_variants", readonly=True)
    size = fields.Char(compute="_compute_fashion_variants", readonly=True)
    color = fields.Char(compute="_compute_fashion_variants", readonly=True)

    @api.depends('product_template_variant_value_ids')
    def _compute_fashion_variants(self):
        for rec in self:
            rec.size = None
            rec.gender = None
            rec.color = None
            if rec.product_template_variant_value_ids:
                for r in rec.product_template_variant_value_ids:
                    if r.attribute_id.type == 'size':
                        rec.size = r.name
                    elif r.attribute_id.type == 'gender':
                        rec.gender = r.name
                    elif r.attribute_id.type == 'color':
                        rec.color = r.name
