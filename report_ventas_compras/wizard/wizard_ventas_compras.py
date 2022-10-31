# -*- coding: utf-8 -*-
import time
from datetime import datetime
from dateutil import relativedelta
from odoo import models, fields, api


class WizardVentasCompras(models.TransientModel):
    _name = 'wizard.ventas.compras'

    def _revisar_diario(self):
        return self.env.context('active_id', None)

    company_id = fields.Many2one(
        'res.company', 'Empresa', required=True,
        default=lambda self: self.env.company)
    journal_ids = fields.Many2many(
        'account.journal', 'book_journal_rel', 'wizard_id', 'journal_id',
        'Diarios', required=True)
    tax_id = fields.Many2one(
        'account.tax.group', 'Impuesto', required=True,
        default=lambda self: self.env['account.tax.group'].search(
            [], limit=1).id)
    base_id = fields.Many2one(
        'account.tax.group', 'Base', required=True,
        default=lambda self: self.env['account.tax.group'].search(
            [], limit=1).id)
    folio_inicial = fields.Integer(required=True, default=1)
    date_from = fields.Date(
        'Fecha desde', required=True,
        default=lambda *a: time.strftime('%Y-%m-01'))
    date_to = fields.Date(
        'Fecha hasta', required=True,
        default=str(datetime.now() + relativedelta.relativedelta(
            months=+1, day=1, days=-1))[:10])
    type_book = fields.Selection(
        [('sale', 'Sale'),
         ('purchase', 'Purchase')],
        required=True,
        default="sale", readonly=True)
    type_report = fields.Selection(
        [('pdf', 'PDF'),
         ('xls', 'XLS')],
        required=True,
        default="pdf")
    currency_id = fields.Many2one('res.currency', string='Moneda', store=True, required=True, compute='_compute_currency_id')
    
    @api.depends('company_id')
    def _compute_currency_id(self):
        for order in self:
            order.currency_id = order.company_id.currency_id if order.company_id else False

    @api.onchange('type_book')
    def _change_type_book_domain_journal_ids(self):
        """Force domain for the 'journal_id' field"""
        self.journal_ids = [(6, 0, [])]
        domain = [('type', 'in', ['sale', 'sale_refund', 'cash'])]
        if self.type_book == 'purchase':
            domain = [('type', 'in', ['purchase', 'purchase_refund'])]
        return {'domain': {'journal_ids': domain}}

    def print_report(self):
        datas = {}
        datas['form'] = self.read(['company_id', 'journal_ids', 'tax_id',
                                   'base_id', 'folio_inicial', 'date_from',
                                   'date_to'])[0]
        report_name = 'report_ventas_compras.report_purchase_book'
        if self.type_report == 'xls' and self.type_book == 'purchase':
            report_name = 'report_ventas_compras.purchase_book_xls'
        elif self.type_report == 'xls' and self.type_book == 'sale':
            report_name = 'report_ventas_compras.sale_book_xls'
        elif self.type_book == 'sale':
            report_name = 'report_ventas_compras.report_sale_book'
        return self.env['report'].get_action([], report_name, data=datas)

    def print_report_sale(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': self.id,
            'model': 'wizard.ventas.compras',
            'form': data,
        }
        return self.env.ref('report_ventas_compras.report_sale_book_ab').report_action(self, data=datas)
    
    def print_report_sale_xls(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': self.id,
            'model': 'wizard.ventas.compras',
            'form': data,
        }
        return self.env.ref('report_ventas_compras.report_sale_book_ab_xls').report_action(self, data=datas)

    def print_report_purchase(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': self.id,
            'model': 'wizard.ventas.compras',
            'form': data,
        }
        return self.env.ref('report_ventas_compras.report_purchase_book_ab').report_action(self, data=datas)

    def print_report_purchase_xls(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': self.id,
            'model': 'wizard.ventas.compras',
            'form': data,
        }
        return self.env.ref('report_ventas_compras.report_purchase_book_ab_xls').report_action(self, data=datas)
