# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
class ProductProduct(models.Model):
    _inherit = 'product.product'
    volume = fields.Float('Volume', digits=(8,5))

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    rate_ctn = fields.Float(string="Cant. Fardo")
    inner_qty = fields.Integer(string="Inner")
    #Sobre escribiendo campo volume, para incluir mas decimales
    volume = fields.Float(
        'Volume', compute='_compute_volume', inverse='_set_volume', digits=(8,5), store=True)
    
    

class SaleOrderCancel(models.TransientModel):
    _name = 'sale.order.cancel'
    _description = "Sales Order Cancel"

    order_id = fields.Many2one('sale.order', string='Sale Order', required=True, ondelete='cascade')
    display_invoice_alert = fields.Boolean('Invoice Alert', compute='_compute_display_invoice_alert')

    @api.depends('order_id')
    def _compute_display_invoice_alert(self):
        pass
        #for wizard in self:
        #    wizard.display_invoice_alert =False # bool(wizard.order_id.invoice_ids.filtered(lambda inv: inv.state == 'draft'))

    def action_cancel(self):
        pass
        #return self.order_id.with_context({'disable_cancel_warning': False}).action_cancel()
