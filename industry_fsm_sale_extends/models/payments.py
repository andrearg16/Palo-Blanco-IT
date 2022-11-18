from odoo import models, fields, api, _

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    invoice_ids = fields.Many2many('account.move', 'account_invoice_payment_rel', 'payment_id', 'invoice_id', string="Invoices", copy=False)
    
    def action_print(self):
        self.ensure_one()
        return self.env.ref('kal_ticket_payment.action_custom_receipt_payment_report').report_action(self)

    @api.model
    def create(self, vals):
        res = super(AccountPayment, self).create(vals)
        # Recorre facturas relacionadas al pago (account_move)
        for inv in res.invoice_ids:
            price = vals['amount']
            if vals['currency_id']!=inv.currency_id:
                price = inv.currency_id._convert(
                                from_amount=vals['amount'], 
                                to_currency=inv.company_id.currency_id,
                                company=inv.company_id,
                                date=vals['date']
                            )
            inv.pending_apply = inv.pending_apply + price
            #inv.expected_due = inv.amount_residual_signed - inv.pending_apply 

        return res

class AccountMove(models.Model):
    _inherit = 'account.move'
    pending_apply = fields.Monetary(string="Pendiente de Aplicar")
    expected_due = fields.Monetary(string="Adeudado Previsto", compute='_update_pending_apply')

    @api.depends('pending_apply','amount_residual_signed')
    def _update_pending_apply(self):
        for rec in self:
            if rec.pending_apply:
                rec.expected_due = rec.amount_residual_signed - rec.pending_apply
            else:
                rec.expected_due = rec.amount_residual_signed