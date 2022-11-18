# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

try:
    from num2words import num2words
except:
    raise UserError(_("run Command: 'pip install num2words'"))


_logger = logging.getLogger( __name__ )

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    approved_by_id = fields.Many2one('res.users', string="Aprobado por")

    def button_approve(self, force=False):
        result = super(PurchaseOrder,self).button_approve(force=False)
        for rec in self:
            rec.approved_by_id = self.env.user.id
        return result

    def get_num2words(self, amount, lang='en'):
        words = num2words(amount, lang=lang, to='currency') 
        words = words.capitalize()
        #CONVERSIÓN DE MONEDA 
        if self.currency_id.name =='USD':
            result = words.replace("euro", "Dolare")
            result = result.replace("céntimo", "centavo")
        elif self.currency_id.name =='GTQ':
            result = words.replace("euro", "Quetzale")
        #conversión por lenguaje
        if self.partner_id.lang =='en_US':
            result = result.replace("Dolare", "dolars")
            result = result.replace("Quetzale", "quetzals")

        return result

    title_code = fields.Char(string="Código")
    comments = fields.Text("Comments")
    
    @api.constrains('title_code')
    def _check_title_code(self):
        for rec in self:
            order_ids = self.env['purchase.order'].search([('title_code', '=', rec.title_code), ('id', '!=', self.id)])
            if order_ids and len(order_ids.ids) > 0:
                raise ValidationError(("No se puede crear una Compra con el mismo codigo %s") %(rec.title_code))

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    ctn = fields.Float(string="Ctn",digits=(8,5))
    rate_ctn = fields.Float(string="Unds. Fardo")
    cbm = fields.Float(string="CBM", compute="_compute_cbm")
    pb_kgs = fields.Float(string="PB KGS", compute="_compute_pb_kgs")
                
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
    
    @api.onchange('product_id')
    def _onchange_product_rate_ctn(self):
        if self.product_id:
            self.rate_ctn = self.product_id.rate_ctn

    # Verificado CNT* UNIS FARDO = CANTIDAD
    @api.onchange('ctn', 'rate_ctn')
    def _compute_product_qty_from_ctm(self):
        for line in self:
            line.product_qty = line.ctn * line.rate_ctn

   # Verificado  Correcto CANTIDAD / UND FARDO = CNT
    @api.onchange('product_qty', 'rate_ctn')
    def _compute_ctn_from_product_qty(self):
        try:
            for line in self:
                line.ctn = line.product_qty / line.rate_ctn
        except ZeroDivisionError:
            line.ctn = 0.0

      
