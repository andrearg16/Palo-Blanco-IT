# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019 Xetechs, S.A. (<https://www.xetechs.com>).
#
#    For Module Support : laquino@xetechs.com --> Luis Aquino + 502 4814-3481
#
##############################################################################

import string
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    arancel_id = fields.Many2one('product.arancel', 'Arancel', required=False)
    import_calculation  = fields.Selection([
        ('dai', 'Autocalcular DAI'),
        ('cbm', 'Autocalcular CM'),
        ('seguro', 'Autocalcular Seguro')], 'Autocalcular', required=False)
    last_cost = fields.Float(string="Ultimo Coste")

ProductTemplate()

class ProductArancel(models.Model):
    _name = "product.arancel"
    _description = "Tabla de aranceles en productos"

    name = fields.Char('Arancel', compute="_compute_name")
    amount_arancel = fields.Float('Porcentaje (%)', required=True, help="Monto porcentual del arancel a aplicar")
    notes = fields.Text('Descripcion', required=False, help="Descripcion del arancel")

    @api.depends('notes', 'amount_arancel')
    def _compute_name(self):
        display_name = ""
        for rec in self:
            if rec.notes:
                display_name = (("%s %s") %(rec.notes, rec.amount_arancel))
            else:
                display_name = (("%s %s") %(rec.amount_arancel, "(%)"))
            rec.update({
                'name': display_name or "",
            })

ProductArancel()