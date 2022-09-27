from odoo import models, fields, api


class SProductAttribute(models.Model):
    _inherit = 'product.attribute'
    type = fields.Selection([
        ('gender', 'Gender'),
        ('size', 'Size'),
        ('color', 'Color'),
        ('other', 'Other'),
    ], string='Type', default='other')
