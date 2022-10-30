# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    factura_cambiaria = fields.Boolean('Factura Cambiaria')
    is_fel = fields.Boolean('¿Activar FEL?', required=False, default=False)
    codigo_est = fields.Char(string='Codigo Establecimiento', help='Número del establecimiento donde se emite el documento. Es el que aparece asignado por SAT en sus registros.')
    is_factura_especial = fields.Boolean('Factura Especial', required=False, default=False)

class AccountTax(models.Model):
    _inherit = "account.tax"

    active_fel = fields.Boolean('Factura Especial', required=False, default=False)
    type_fel = fields.Selection([('RETEN_IVA', 'Retencion FE IVA'), ('RETEN_ISR', 'Retencion FE ISR')], string="Tipo Retencion")

class AccountTaxGroup(models.Model):
    _inherit = "account.tax.group"

    fel_code = fields.Char('Etiqueda FEL', required=False)