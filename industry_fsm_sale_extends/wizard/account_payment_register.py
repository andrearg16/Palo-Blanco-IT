# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, RedirectWarning
from odoo.tools.misc import formatLang, format_date

INV_LINES_PER_STUB = 9


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"
    numero_transaccion = fields.Char(string='Numero de Transaccion')

    def _create_payments(self):
        self.ensure_one()
        context = self.env.context
        if context.get('params'):
            params = context['params']
            if params['model'] == 'project.task':
                project_task_id = params.get("id")
                account_move = self.env['account.move'].search([('id', '=', context['active_id'])])
                batches = self._get_batches()
                edit_mode = self.can_edit_wizard and (len(batches[0]['lines']) == 1 or self.group_payment)

                to_reconcile = []
                if edit_mode:
                    payment_vals = self._create_payment_vals_from_wizard()
                    payment_vals_list = [payment_vals]
                    to_reconcile.append(batches[0]['lines'])
                else:
                    # Don't group payments: Create one batch per move.
                    if not self.group_payment:
                        new_batches = []
                        for batch_result in batches:
                            for line in batch_result['lines']:
                                new_batches.append({
                                    **batch_result,
                                    'lines': line,
                                })
                        batches = new_batches

                    payment_vals_list = []
                    for batch_result in batches:
                        payment_vals_list.append(self._create_payment_vals_from_batch(batch_result))
                        to_reconcile.append(batch_result['lines'])

                payments = self.env['account.payment'].create(payment_vals_list)

                # If payments are made using a currency different than the source one, ensure the balance match exactly in
                # order to fully paid the source journal items.
                # For example, suppose a new currency B having a rate 100:1 regarding the company currency A.
                # If you try to pay 12.15A using 0.12B, the computed balance will be 12.00A for the payment instead of 12.15A.
                if edit_mode:
                    for payment, lines in zip(payments, to_reconcile):
                        # Batches are made using the same currency so making 'lines.currency_id' is ok.
                        if payment.currency_id != lines.currency_id:
                            liquidity_lines, counterpart_lines, writeoff_lines = payment._seek_for_lines()
                            source_balance = abs(sum(lines.mapped('amount_residual')))
                            payment_rate = liquidity_lines[0].amount_currency / liquidity_lines[0].balance
                            source_balance_converted = abs(source_balance) * payment_rate

                            # Translate the balance into the payment currency is order to be able to compare them.
                            # In case in both have the same value (12.15 * 0.01 ~= 0.12 in our example), it means the user
                            # attempt to fully paid the source lines and then, we need to manually fix them to get a perfect
                            # match.
                            payment_balance = abs(sum(counterpart_lines.mapped('balance')))
                            payment_amount_currency = abs(sum(counterpart_lines.mapped('amount_currency')))
                            if not payment.currency_id.is_zero(source_balance_converted - payment_amount_currency):
                                continue

                            delta_balance = source_balance - payment_balance

                            # Balance are already the same.
                            if self.company_currency_id.is_zero(delta_balance):
                                continue

                            # Fix the balance but make sure to peek the liquidity and counterpart lines first.
                            debit_lines = (liquidity_lines + counterpart_lines).filtered('debit')
                            credit_lines = (liquidity_lines + counterpart_lines).filtered('credit')

                            payment.move_id.write({'line_ids': [
                                (1, debit_lines[0].id, {'debit': debit_lines[0].debit + delta_balance}),
                                (1, credit_lines[0].id, {'credit': credit_lines[0].credit + delta_balance}),
                            ]})
                project_id = self.env['project.task'].search([('id', '=', project_task_id)])
                project_id.write({'payment_ids': [(4, payment.id)]})
                return payments
        return super(AccountPaymentRegister, self)._create_payments()


class AccountPayment(models.Model):
    _inherit = "account.payment"

    project_task_id = fields.Many2one('project.task', string="Visita asociada")
    factura_asociada = fields.Many2one('account.invoice', string="Factura asociada")
    numero_transaccion = fields.Char(string="Número de transacción")


