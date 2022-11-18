# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def get_simple_name(self):
        if self.product_id:
            if self.default_code:
                default_code = '[code]'.format(self.default_code)
                product_name = self.name.replace(default_code, '')
                return product_name
        return self.name

class ProductPriceList(models.Model):
    _inherit = 'product.pricelist'

    def delete_pricelist_item(self):
        for record in self:
            for item in record.item_ids:
                item.unlink()

class SaleOrder(models.Model):
    _inherit='sale.order'

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    ctn = fields.Float(string="Ctn",digits=(0,0))
    rate_ctn = fields.Float(string="Unds. Fardo",digits=(0,0))
    cbm = fields.Float(string="CBM", compute="_compute_cbm",digits=(12,5))
    pb_kgs = fields.Float(string="PB KGS", compute="_compute_pb_kgs",digits=(0,0))
    inner = fields.Float(string="Inner",digits=(0,0))
    inner_qty = fields.Integer(string="Unidades Inner", related='product_id.inner_qty')
    product_uom_qty = fields.Float(string='Quantity', digits=(0,0), required=True, default=1)       
    
    @api.onchange('product_uom_qty')
    def _onchange_qty(self):
        try:
            self.rate_ctn = self.product_id.rate_ctn
            self.inner = self.product_uom_qty/self.product_id.inner_qty
            self.ctn = self.product_uom_qty / self.rate_ctn 
        except ZeroDivisionError:
            self.inner = 0
            self.ctn = 0
                
    @api.onchange('inner')
    def _compute_product_uom_qty_from_inner(self):
        self.product_uom_qty = self.product_id.inner_qty * self.inner 
        
    @api.onchange('ctn')
    def _compute_product_uom_qty_from_ctn(self):
        self.product_uom_qty = self.ctn * self.rate_ctn
        
    @api.onchange('product_id', 'rate_ctn')
    def _compute_cbm(self):
        for rec in self:
            if rec.ctn > 0:
                rec.cbm = rec.ctn * rec.product_id.volume
            else:
                rec.cbm = 0

    @api.onchange('product_id', 'rate_ctn')
    def _compute_pb_kgs(self):
        for rec in self:
            if rec.ctn > 0:
                rec.pb_kgs = rec.ctn * rec.product_id.weight
            else:
                rec.pb_kgs = 0