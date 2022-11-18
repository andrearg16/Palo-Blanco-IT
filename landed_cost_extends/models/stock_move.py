# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019 Xetechs, S.A. (<https://www.xetechs.com>).
#
#    For Module Support : laquino@xetechs.com --> Luis Aquino + 502 4814-3481
#
##############################################################################

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    container_qty = fields.Float('No. Contenedor', required=False, default=1.00)
    is_manual_rate = fields.Boolean('¿Tasa de cambio manual?', required=False, default=False)
    manual_rate = fields.Float('Tasa de Cambio', digits=(12, 6))


class StockMove(models.Model):
    _inherit = 'stock.move'
    cbm_qty = fields.Float('CBM Total', required=False, help="CBM total para el producto")
    cbm_price = fields.Float('Costo x CBM', required=False, help="Costo unitario por CBM")
    currency_id = fields.Many2one('res.currency', 'Moneda', related="purchase_line_id.currency_id")
    total_cbm = fields.Float('Flete Maritimo', compute="_compute_cost", store=False)
    total_cbm_qtq = fields.Float('Flete Maritimo GTQ', compute="_compute_cost", store=False)
    total_purchase = fields.Float('Total compra', compute="_compute_cost", store=False)
    currency_rate = fields.Float('TC', compute="_compute_rate", digits=(12, 6), store=True)
    price_unit_purchase = fields.Float('Precio Unitario', related="purchase_line_id.price_unit")
    amount_seguro = fields.Float('Seguro (%)', required=False, default=0.00)
    total_seguro = fields.Float('Total Seguro', compute="_compute_cost", store=False)
    amount_dai = fields.Float('DAI (%)', compute="_compute_dai")
    total_dai = fields.Float('Total DAI', compute="_compute_cost", store=False)
    amount_total = fields.Float('Total QTQ', compute="_compute_cost", store=False)

    @api.depends('product_id')
    def _compute_dai(self):
        dai = 0.00
        for rec in self:
            if rec.product_id and rec.product_id.arancel_id:
                dai = rec.product_id.arancel_id.amount_arancel
            else:
                dai = 0.00
            rec.update({
                'amount_dai': dai or 0.00
            })

    @api.depends('picking_id.manual_rate', 'picking_id.is_manual_rate', 'currency_id')
    def _compute_rate(self):
        for rec in self:
            if rec.picking_id.is_manual_rate and rec.picking_id.manual_rate != 0:
                rec.currency_rate = rec.picking_id.manual_rate or 1
            else:
                if rec.currency_id.rate != 0:
                    rec.currency_rate = 1 / rec.currency_id.rate

    @api.depends('cbm_qty', 'cbm_price', 'currency_id', 'currency_rate', 'picking_id.is_manual_rate', 'price_unit', 'product_uom_qty', 'amount_seguro', 'amount_dai')
    def _compute_cost(self):
        for rec in self:
            rec.total_cbm = (rec.cbm_qty * rec.cbm_price)
            # rec.total_cbm_qtq = (rec.cbm_qty * rec.cbm_price) * rec.currency_rate
            rec.total_purchase = (rec.product_uom_qty * rec.price_unit_purchase)
            rec.total_cbm_qtq = (rec.cbm_qty * rec.cbm_price) * rec.currency_rate
            rec.amount_total = ((rec.cbm_qty * rec.cbm_price) + rec.total_purchase) * rec.currency_rate
            rec.total_seguro = ((rec.amount_total * rec.amount_seguro) / 100)
            rec.total_dai = (((rec.price_unit_purchase * rec.currency_rate) * rec.amount_dai) / 100)
