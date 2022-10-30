# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    computed_taxes = fields.Monetary(compute="_computed_taxes")
    no_fe_taxes = fields.Float(compute="_no_fe_taxes")
    fe_total_line_amount = fields.Monetary(compute="_fe_total_line_amount")

    def _computed_taxes(self):
        for data in self:
            data.computed_taxes = round(data.price_total - data.price_subtotal, 2)

    def _no_fe_taxes(self):
        for data in self:
            if data.tax_ids and data.move_id.journal_id.is_factura_especial:
                for tax in data.tax_ids:
                    if not tax.active_fel and tax.amount == 12:
                        data.no_fe_taxes = round(data.price_subtotal * 12 / 100, 2)
            else:
                data.no_fe_taxes = 0

    def _fe_total_line_amount(self):
        for data in self:
            data.fe_total_line_amount = data.price_total
            if data.tax_ids and data.move_id.journal_id.is_factura_especial:
                for tax in data.tax_ids:
                    if tax.active_fel and tax.type_fel in ['RETEN_IVA', 'RETEN_ISR']:
                        data.fe_total_line_amount += (abs(tax.amount)/100) * data.price_subtotal
            data.fe_total_line_amount = round(data.fe_total_line_amount, 2)

