# -*- coding: utf-8 -*-
from odoo import models, fields

class WizardShowPayments(models.TransientModel):
    _name = 'wizard.show.payments'
    move_id = fields.Many2one('account.move', string="Factura")
    payment_id = fields.Many2many('account.payment', string="Pagos", required=True)
    partner_name = fields.Char(related="payment_id.partner_id.name", string="Cliente")
    partner_vat = fields.Char(related="payment_id.partner_id.vat", string="Nit")
    partner_ref = fields.Char(related="payment_id.partner_id.ref", string="Ref")
    partner_credit = fields.Monetary(related="payment_id.partner_id.credit", string="Credito")
    payment_date = fields.Date(related="payment_id.date", string="Fecha")
    currency_id = fields.Many2one("res.currency", related="payment_id.currency_id", string="Moneda")
    journal_name = fields.Char(related="payment_id.journal_id.name", string="Diario")
    currency_name = fields.Char(related="payment_id.currency_id.symbol", string="Moneda")
    amount = fields.Monetary(related="payment_id.amount", string="Monto")
    ref = fields.Char(related="payment_id.ref", string="Ref")   
    invoice_ids = fields.Many2many(related="payment_id.invoice_ids", string="Facturas") 
    
    def print_report(self):
        data = {
            'form': self.read()[0],
            'payments': self.payment_id,
            'partner_name': self.partner_name,
            'partner_vat': self.partner_vat,
            'partner_ref': self.partner_ref,
            'partner_credit': self.partner_credit,
            'payment_date': self.payment_date,
            'journal_name': self.journal_name,
            'currency_name': self.currency_name,
            'amount': self.amount,
            'ref': self.ref,
            'invoice_ids': self.invoice_ids,
        }
        return self.env.ref('kal_ticket_payment.action_custom_receipt_payment_report_wizard').report_action(self, data=data)
