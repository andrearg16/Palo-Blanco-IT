# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
import logging

_logger = logging.getLogger( __name__ )


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'frase_ids': self.env['satdte.frases'].search([('name', '=', 'Sujeto a pagos trimestrales ISR')]).ids,
        })
        return invoice_vals
    
class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    
    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        invoice_vals.update({
            'frase_ids': self.env['satdte.frases'].search([('name', '=', 'Sujeto a pagos trimestrales ISR')]).ids,
        })
        return invoice_vals