# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomProduct(models.Model):
    _inherit = 'product.template'

    delivery_pending = fields.Float(string="Pendiente de entrega", compute="get_delivery_pending")
    monthly_sale = fields.Float(string="Venta Mensual", compute="get_monthly_sale")
    existence_trans = fields.Float(string="Existencia trans.", compute="get_existence_trans")
    days_inv = fields.Float(string="Días inv.", compute="get_days_inv")
    transit = fields.Float(string="Tránsito", compute="get_transit")

    @api.depends('transit')
    def get_transit(self):
        company_id = self.env.user.company_id.id
        for record in self:
            product_id = record.env['product.product'].search([('product_tmpl_id', '=', record.id)]).id
            record.env.cr.execute("""
                        select sum(product_qty) as product_qty from stock_move_line where 
                        product_id = """ + str(product_id) + """ and picking_id in
                        (select id from stock_picking where company_id = """ + str(company_id) + """ 
                        and picking_type_id = 7)
                                """)
            data = record.env.cr.dictfetchall()
            for value in data:
                qty = value['product_qty']
            record.transit = qty

    @api.depends('existence_trans')
    def get_existence_trans(self):
        company_id = self.env.user.company_id.id
        for record in self:
            product_id = record.env['product.product'].search([('product_tmpl_id', '=', record.id)]).id

            record.env.cr.execute("""
                            SELECT quantity FROM stock_quant WHERE product_id = """ + str(product_id) + """
                            AND company_id = """ + str(company_id) + """
                            AND location_id = 8
                                    """)
            data = record.env.cr.dictfetchall()
            if data:
                for value in data:
                    qty_available = value['quantity']
                record.existence_trans = qty_available
            else:
                record.existence_trans = 0.0

    @api.depends('delivery_pending')
    def get_delivery_pending(self):
        company_id = self.env.user.company_id.id
        for record in self:
            product_id = record.env['product.product'].search([('product_tmpl_id', '=', record.id)]).id
            record.env.cr.execute("""
                                select sum(product_qty) as product_qty from stock_move_line where 
                                product_id = """ + str(product_id) + """ and picking_id in
                                (select id from stock_picking where company_id = """ + str(company_id) + """
                                and picking_type_id = 8)
                                        """)
            data = record.env.cr.dictfetchall()
            for value in data:
                pending = value['product_qty']
            record.delivery_pending = pending

    @api.depends('monthly_sale')
    def get_monthly_sale(self):
        company_id = self.env.user.company_id.id
        for record in self:
            product_id = record.env['product.product'].search([('product_tmpl_id', '=', record.id)]).id
            record.env.cr.execute("""
                        select sum(qty_done) as qty_done from stock_move_line where 
                        product_id = """ + str(product_id) + """ and picking_id in
                        (select id from stock_picking where company_id = """ + str(company_id) + """ 
                        and picking_type_id = 8 and date > current_date - interval '6 month')
                                """)
            data = record.env.cr.dictfetchall()
            for value in data:
                if value['qty_done'] is None:
                    sale = 0.0
                else:
                    sale = value['qty_done'] / 6
                record.monthly_sale = sale

    @api.depends('days_inv')
    def get_days_inv(self):
        for record in self:
            if record.monthly_sale == 0:
                record.days_inv = 0.0
            else:
                days_inv_value = record.qty_available / record.monthly_sale
                record.days_inv = days_inv_value


class CustomStockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    delivery_pending = fields.Float(string="Pendiente de entrega", compute="get_delivery_pending")
    monthly_sale = fields.Float(string="Venta Mensual", compute="get_monthly_sale")
    existence_trans = fields.Float(string="Existencia trans.", compute="get_existence_trans")
    days_inv = fields.Float(string="Días inv.", compute="get_days_inv")
    transit = fields.Float(string="Tránsito", compute="get_transit")

    def get_transit(self):
        company_id = self.env.user.company_id.id
        for record in self:
            product_id = record.env['product.product'].search([('product_tmpl_id', '=', record.id)]).id

            record.env.cr.execute("""
                        select sum(product_qty) as product_qty from stock_move_line where 
                        product_id = """ + str(record.product_id.id) + """ and picking_id in
                        (select id from stock_picking where company_id = """ + str(company_id) + """ 
                        and picking_type_id = 7)
                                """)
            data = record.env.cr.dictfetchall()
            for value in data:
                qty = value['product_qty']
            record.transit = qty

    @api.depends('existence_trans')
    def get_existence_trans(self):
        company_id = self.env.user.company_id.id
        for record in self:
            record.env.cr.execute("""
                                SELECT quantity FROM stock_quant WHERE product_id = """ + str(record.product_id.id) + """
                                AND company_id = """ + str(company_id) + """
                                AND location_id = 8
                                        """)
            data = record.env.cr.dictfetchall()
            if data:
                for value in data:
                    qty_available = value['quantity']
                record.existence_trans = qty_available
            else:
                record.existence_trans = 0.0

    def get_delivery_pending(self):
        company_id = self.env.user.company_id.id
        for record in self:
            record.env.cr.execute("""
                                select sum(product_qty) as product_qty from stock_move_line where 
                                product_id = """ + str(record.product_id.id) + """ and picking_id in
                                (select id from stock_picking where company_id = """ + str(company_id) + """
                                and picking_type_id = 8)
                                        """)
            data = record.env.cr.dictfetchall()
            for value in data:
                pending = value['product_qty']
            record.delivery_pending = pending

    def get_monthly_sale(self):
        company_id = self.env.user.company_id.id
        for record in self:
            record.env.cr.execute("""
                        select sum(qty_done) as qty_done from stock_move_line where 
                        product_id = """ + str(record.product_id.id) + """ and picking_id in
                        (select id from stock_picking where company_id = """ + str(company_id) + """ 
                        and picking_type_id = 8 and date > current_date - interval '6 month')
                                """)
            data = record.env.cr.dictfetchall()
            for value in data:
                if value['qty_done'] is None:
                    sale = 0.0
                else:
                    sale = value['qty_done'] / 6
                record.monthly_sale = sale

    def get_days_inv(self):
        for record in self:
            # qty_available = record.env['product.template'].search([('id', '=', record.product_id.id)]).qty_available
            if record.monthly_sale == 0:
                record.days_inv = 0.0
                print('0')
            else:
                days_inv_value = record.qty_on_hand / record.monthly_sale
                record.days_inv = days_inv_value
                print('value')
