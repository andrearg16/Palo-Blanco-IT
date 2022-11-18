from tabnanny import check
from odoo import models, fields, api, _

class PaymentRegisterfrom(models.Model):

    _inherit= 'account.payment'
    payment_date = fields.Date(string="Fecha de cobro")
    check_transfer = fields.Char(string="No. de Transferencia o Cheque")
    invoice_ids = fields.Many2many(
        'account.move', 'account_invoice_payment_rel', 'payment_id', 'invoice_id', 
        string="Invoices", copy=False)

    def action_post(self):
        """
        Herencia a la funcion action_post, si el pago es creado desde las rutas (project.task)
        Traera por defecto la factura, entonces se condiciona para hacer la conciliacion con el pago
        caso contrario solo publica el pago.
        """
        res = super(PaymentRegisterfrom, self).action_post()
        if self.invoice_ids:
            # Resta valor pendiente por que pasa a posted
            for inv in self.invoice_ids:
                price = self.amount
                if self.currency_id!=inv.currency_id:
                    price = inv.currency_id._convert(
                                from_amount=self.amount, 
                                to_currency=inv.company_id.currency_id,
                                company=inv.company_id,
                                date=self.date
                            )
                inv.pending_apply = inv.pending_apply - price

            partner_account = self.partner_id.property_account_receivable_id.id
            for payment_res in self:
                if payment_res.invoice_ids:
                    moves_to_reconcile = []
                    # Recorre las lineas de pago
                    for move in payment_res.move_id.line_ids:
                        if move.account_id.id == partner_account:
                            moves_to_reconcile = []
                            moves_to_reconcile.append(move.id)
                    # Recorre las lineas de la factura
                    for invoice in payment_res.invoice_ids:
                        for move in invoice.line_ids:

                            if move.account_id.id == partner_account:
                                moves_to_reconcile.append(move.id)
                    move_lines = self.env['account.move.line'].search([('id','in',moves_to_reconcile)])
                    # Conciliacion de pago con factura
                    move_lines.reconcile()
        return res
    
    def action_draft(self):
        res = super(PaymentRegisterfrom, self).action_draft()
        if self.invoice_ids:
            # Suma valor pendiente por que pasa a draft
            for inv in self.invoice_ids:
                price = self.amount
                if self.currency_id!=inv.currency_id:
                    price = inv.currency_id._convert(
                                from_amount=self.amount, 
                                to_currency=inv.company_id.currency_id,
                                company=inv.company_id,
                                date=self.date
                            )
                inv.pending_apply = inv.pending_apply + price

        return res


class ListPaymentRegister(models.Model):
    _name='list.payment.register'
    _description = 'Nuevo modelo'
    
    bank_id = fields.Many2one('res.bank', string="Banco", copy=True)
    transfer_register = fields.Char(string="No.Transferencia o Cheque")

class PaymentRegisterWizard(models.TransientModel):

    _inherit= 'account.payment.register'
    payment_date_wizard = fields.Date(string="Fecha de cobro")

    def _post_payments(self, to_process, edit_mode=False):
        """ 
            Herencia para dejar el pago en estado borrador por defecto
        """
        payments = self.env['account.payment']
        for vals in to_process:
            payments |= vals['payment']
        payments.action_draft()


    def _create_payment_vals_from_batch(self, batch_result):
        batch_values = self._get_wizard_values_from_batch(batch_result)
        if batch_values['payment_type'] == 'inbound':
            partner_bank_id = self.journal_id.bank_account_id.id
        else:
            partner_bank_id = batch_result['payment_values']['partner_bank_id']

        return {
            'date': self.payment_date,
            'amount': batch_values['source_amount_currency'],
            'payment_type': batch_values['payment_type'],
            'partner_type': batch_values['partner_type'],
            'ref': self._get_batch_communication(batch_result),
            'invoice_ids': self.line_ids.move_id,
            'payment_date': self.payment_date_wizard,
            'journal_id': self.journal_id.id,
            'currency_id': batch_values['source_currency_id'],
            'partner_id': batch_values['partner_id'],
            'partner_bank_id': partner_bank_id,
            'payment_method_line_id': self.payment_method_line_id.id,
            'destination_account_id': batch_result['lines'][0].account_id.id
        }

    def _create_payment_vals_from_wizard(self):
        payment_vals = {
            'date': self.payment_date,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'ref': self.communication,
            'invoice_ids': self.line_ids.move_id,
            'payment_date': self.payment_date_wizard,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'payment_method_line_id': self.payment_method_line_id.id,
            'destination_account_id': self.line_ids[0].account_id.id
        }

        if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
            payment_vals['write_off_line_vals'] = {
                'name': self.writeoff_label,
                'amount': self.payment_difference,
                'account_id': self.writeoff_account_id.id,
            }
        return payment_vals