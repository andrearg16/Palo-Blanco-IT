# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    inner_qty = fields.Integer(related='product_tmpl_id.inner_qty', readonly=True, copy=False, string="inner_qty")
    rate_ctn = fields.Float(related='product_tmpl_id.rate_ctn',string="Cant. Fardo")