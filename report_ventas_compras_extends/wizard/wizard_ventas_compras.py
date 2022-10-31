# -*- coding: utf-8 -*-
import time
from datetime import datetime
from dateutil import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


import time
import xlwt
import base64
#import io
from io import BytesIO
#import base64

class WizardVentasCompras(models.TransientModel):
    _inherit = 'wizard.ventas.compras'


    file_name = fields.Char('Nombre archivo')
    file = fields.Binary('Archivo', filters='.xls')

    ##@api.multi
    def print_report(self):
        datas = {}
        datas['form'] = self.read(['company_id', 'journal_ids', 'tax_id',
                                   'base_id', 'folio_inicial', 'date_from',
                                   'date_to'])[0]
        #report_name = 'report_ventas_compras.report_purchase_book'
        if self.type_report == 'pdf' and self.type_book == 'sale':
            return self.env['report'].get_action([], 'report_ventas_compras.report_sale_book', data=datas)
        if self.type_report == 'xls' and self.type_book == 'purchase':
            #report_name = 'report_ventas_compras.purchase_book_xls'
            return True
        if self.type_report == 'xls' and self.type_book == 'sale':
            #report_name = 'report_ventas_compras.sale_book_xls'
            self.print_sale_excel()
        if self.type_report == 'pdf' and self.type_book == 'purchase':
            #report_name = 'report_ventas_compras.report_sale_book'
            return self.env['report'].get_action([], 'report_ventas_compras.report_sale_book', data=datas)
        return True
    

    ##@api.multi
    def print_sale_excel(self):
        lang_code = self.env.context.get('lang') or 'en_US'
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        for rec in self:
            if not rec.journal_ids:
                raise UserError(("No hay ningun diario seleccionado..!"))
            libro = xlwt.Workbook()
            hoja = libro.add_sheet('Libro de Ventas')

            titulos_principales_style = xlwt.easyxf('borders: top_color black, bottom_color black, right_color black, left_color black,\
            left thin, right thin, top thin, bottom thin; align: horiz center; font:bold on;')
            titulos_texto_style = xlwt.easyxf('borders: top_color black, bottom_color black, right_color black, left_color black,\
            left thin, right thin, top thin, bottom thin; align: horiz left;')
            titulos_numero_style = xlwt.easyxf('borders: top_color black, bottom_color black, right_color black, left_color black,\
            left thin, right thin, top thin, bottom thin; align: horiz right;')
            company_tittle_style = xlwt.easyxf('align: horiz center; font:bold on;')
            xlwt.add_palette_colour("custom_colour", 0x21)
            libro.set_colour_RGB(0x21, 200, 200, 200)
            #Tittles Styles
            estilo = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour')
            sums_style = xlwt.easyxf('borders: top_color black, bottom_color black, right_color black, left_color black,\
            left thin, right thin, top thin, bottom thin; align: horiz right; font:bold on;')
            hoja.write_merge(0, 0, 0, 16,'LIBRO DE VENTAS Y SERVICIOS', style=company_tittle_style)
            hoja.write_merge(1, 1, 0, 16, rec.company_id.name, style=company_tittle_style)
            hoja.write_merge(2, 2, 0, 16, (("NIT: %s") %(rec.company_id.vat)), style=company_tittle_style)
            hoja.write_merge(3, 3, 0, 16, rec.company_id.street, style=company_tittle_style)
            date_from = datetime.strptime(str(rec.date_from), DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
            date_to = datetime.strptime(str(rec.date_to), DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
            hoja.write_merge(4, 4, 0, 16, (("Del %s Al %s") %(date_from, date_to)), style=company_tittle_style)
            #Encabezados
            y = 8
            hoja.write_merge(y, y, 7, 10, 'Locales', style=titulos_principales_style)
            hoja.write_merge(y, y, 11, 14, 'Exportaciones', style=titulos_principales_style)
            y = 9
            hoja.write_merge(y, y, 7, 8, 'Gravadas', style=titulos_principales_style)
            hoja.write_merge(y, y, 9, 10, 'Exentas', style=titulos_principales_style)
            hoja.write_merge(y, y, 11, 12, 'Gravadas', style=titulos_principales_style)
            hoja.write_merge(y, y, 13, 14, 'Exentas', style=titulos_principales_style)
            y = 10
            hoja.write(y, 0, 'No', style=titulos_principales_style)
            hoja.write(y, 1, 'Fecha', style=titulos_texto_style)
            hoja.write(y, 2, 'Tipo', style=titulos_texto_style)
            hoja.write(y, 3, 'Serie', style=titulos_principales_style)
            hoja.write(y, 4, 'Numero', style=titulos_principales_style)
            hoja.write(y, 5, 'NIT', style=titulos_texto_style)
            hoja.write(y, 6, 'Cliente', style=titulos_principales_style)
            hoja.write(y, 7, 'Bienes', style=titulos_principales_style)
            hoja.write(y, 8, 'Servicios', style=titulos_principales_style)
            hoja.write(y, 9, 'Bienes', style=titulos_principales_style)
            hoja.write(y, 10, 'Servicios', style=titulos_principales_style)
            hoja.write(y, 11, 'Bienes', style=titulos_principales_style)
            hoja.write(y, 12, 'Servicios', style=titulos_principales_style)
            hoja.write(y, 13, 'Bienes', style=titulos_principales_style)
            hoja.write(y, 14, 'Servicios', style=titulos_principales_style)
            hoja.write(y, 15, 'IVA', style=titulos_principales_style)
            hoja.write(y, 16, 'Total', style=titulos_principales_style)
            #Generate Records
            values, summary = rec.generate_records()
            item = 0
            init_rows = y
            for linea in values:
                y += 1
                item += 1
                hoja.write(y, 0, item, style=titulos_texto_style)
                hoja.write(y, 1, linea['fecha'], style=titulos_texto_style)
                hoja.write(y, 2, linea['tipo'], style=titulos_texto_style)
                hoja.write(y, 3, linea['serie'], style=titulos_texto_style)
                hoja.write(y, 4, linea['numero'], style=titulos_texto_style)
                hoja.write(y, 5, linea['nit_cliente'], style=titulos_texto_style)
                hoja.write(y, 6, linea['cliente'], style=titulos_texto_style)
                hoja.write(y, 7, linea['bienes_gravados'], style=titulos_numero_style)
                hoja.write(y, 8, linea['servicios_gravados'], style=titulos_numero_style)
                hoja.write(y, 9, linea['bienes_exentos'], style=titulos_numero_style)
                hoja.write(y, 10, linea['servicios_exentos'], style=titulos_numero_style)
                hoja.write(y, 11, linea['bienes_e_gravados'], style=titulos_numero_style)
                hoja.write(y, 12, linea['servicios_e_gravados'], style=titulos_numero_style)
                hoja.write(y, 13, linea['bienes_e_exentos'], style=titulos_numero_style)
                hoja.write(y, 14, linea['servicios_e_exentos'], style=titulos_numero_style)
                hoja.write(y, 15, linea['iva'], style=titulos_numero_style)
                hoja.write(y, 16, linea['subtotal'], style=titulos_numero_style)
            y += 1
            #Sum on numeric cell
            hoja.write(y, 6, "*TOTALES*", style=sums_style)
            hoja.write(y, 7, xlwt.Formula((("sum(H%s:H%s)") %(init_rows, y))) , style=sums_style)
            hoja.write(y, 8, xlwt.Formula((("sum(I%s:I%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 9, xlwt.Formula((("sum(J%s:J%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 10, xlwt.Formula((("sum(K%s:K%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 11, xlwt.Formula((("sum(L%s:L%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 12, xlwt.Formula((("sum(M%s:M%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 13, xlwt.Formula((("sum(N%s:N%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 14, xlwt.Formula((("sum(O%s:O%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 15, xlwt.Formula((("sum(P%s:P%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 16, xlwt.Formula((("sum(Q%s:Q%s)") %(init_rows, y))), style=sums_style)
            #Summary report
            #Summary header
            y += 3
            hoja.write(y, 6, "", style=titulos_principales_style)
            hoja.write(y, 7, "GRAVADO" , style=titulos_principales_style)
            hoja.write(y, 8, "EXENTO", style=titulos_principales_style)
            hoja.write(y, 9, "IVA", style=titulos_principales_style)
            hoja.write(y, 10, "TOTAL", style=titulos_principales_style)
            y += 1
            hoja.write(y, 6, "BIENES", style=titulos_principales_style)
            hoja.write(y, 7, summary.get('total_bienes_gravados', 0.00) , style=titulos_numero_style)
            hoja.write(y, 8, summary.get('total_bienes_exentos', 0.00), style=titulos_numero_style)
            hoja.write(y, 9, summary.get('total_bienes_iva', 0.00), style=titulos_numero_style)
            hoja.write(y, 10, summary.get('total_bienes', 0.00), style=titulos_numero_style)
            y += 1
            hoja.write(y, 6, "SERVICIOS", style=titulos_principales_style)
            hoja.write(y, 7, summary.get('total_servicios_gravados', 0.00) , style=titulos_numero_style)
            hoja.write(y, 8, summary.get('total_servicios_exentos', 0.00), style=titulos_numero_style)
            hoja.write(y, 9, summary.get('total_servicios_iva', 0.00), style=titulos_numero_style)
            hoja.write(y, 10, summary.get('total_servicios', 0.00), style=titulos_numero_style)
            y += 1
            hoja.write(y, 6, "EXPORTACIONES", style=titulos_principales_style)
            hoja.write(y, 7, summary.get('total_expo_gravados', 0.00) , style=titulos_numero_style)
            hoja.write(y, 8, summary.get('total_expo_exentos', 0.00), style=titulos_numero_style)
            hoja.write(y, 9, summary.get('total_expo_iva', 0.00), style=titulos_numero_style)
            hoja.write(y, 10, summary.get('total_expor', 0.00), style=titulos_numero_style)
            y += 1
            hoja.write(y, 6, "NC", style=titulos_principales_style)
            hoja.write(y, 7, summary.get('total_nc_gravados', 0.00) , style=titulos_numero_style)
            hoja.write(y, 8, summary.get('total_nc_exentos', 0.00), style=titulos_numero_style)
            hoja.write(y, 9, summary.get('total_nc_iva', 0.00), style=titulos_numero_style)
            hoja.write(y, 10, summary.get('total_nc', 0.00), style=titulos_numero_style)
            y += 1
            hoja.write(y, 6, "ND", style=titulos_principales_style)
            hoja.write(y, 7, summary.get('total_nd_gravados', 0.00) , style=titulos_numero_style)
            hoja.write(y, 8, summary.get('total_nd_exentos  ', 0.00), style=titulos_numero_style)
            hoja.write(y, 9, summary.get('total_nd_iva', 0.00), style=titulos_numero_style)
            hoja.write(y, 10, summary.get('total_nd', 0.00), style=titulos_numero_style)
            y += 1
            hoja.write(y, 6, "*TOTALES*", style=titulos_principales_style)
            hoja.write(y, 7, summary.get('total_gravado', 0.00) , style=sums_style)
            hoja.write(y, 8, summary.get('total_exento  ', 0.00), style=sums_style)
            hoja.write(y, 9, summary.get('total_iva', 0.00), style=sums_style)
            hoja.write(y, 10, summary.get('total_total', 0.00), style=sums_style)
            #Save Excel in Wizard
            fp = BytesIO()
            libro.save(fp)
            fp.seek(0)
            report_data_file = base64.encodestring(fp.read())
            fp.close()
            self.write({'file': report_data_file})
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=wizard.ventas.compras&field=file&download=true&id=%s&filename=libro_ventas.xls' % (rec.id),
            'target': 'new',
        }


    #@api.multi
    def generate_records(self):
        result = []
        lang_code = self.env.context.get('lang') or 'en_US'
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        total_iva = 0.00
        total_bienes_gravados = 0.00
        total_bienes_exentos = 0.00
        total_bienes_iva = 0.00
        total_bienes = 0.00
        total_serv_gravados = 0.00
        total_serv_exentos = 0.00
        total_serv_iva = 0.00
        # total_serv = 0.00
        total_expo_gravados = 0.00
        total_expo_exentos = 0.00
        total_expo_iva = 0.00
        # total_expo = 0.00
        total_nc_gravados = 0.00
        total_nc_exentos = 0.00
        total_nc_iva = 0.00
        total_nc = 0.00
        total_nd_gravados = 0.00
        total_nd_exentos = 0.00
        total_nd_iva = 0.00
        total_nd = 0.00
        journal_ids = self.journal_ids.ids or False
        date_from = self.date_from
        date_to = self.date_to
        # tax_ids = tax.search(
        #     ['|', ('tax_group_id', '=', data['form']['tax_id'][0]),
        #      ('tax_group_id', '=', data['form']['tax_id'][0]),
        #      ('type_tax_use', '=', 'purchase')]).mapped('id')
        empresa = self.company_id or False
        folio = self.folio_inicial
        for j in journal_ids:
            facturas = self.env['account.move'].search(
                [('state', 'in', ['posted', 'cancel']),
                    ('journal_id', '=', j),
                    ('invoice_date', '>=', date_from),
                    ('invoice_date', '<=', date_to),
                    ('company_id', '=', empresa.id)], order='name')
            establecimientos = ", ".join([
                jou.name for jou in self.env['account.journal'].browse(
                    journal_ids)])

            for inv in facturas:
                bien_local_gravado = 0.00
                servicio_local_gravado = 0.00
                bien_local_exento = 0.00
                servicio_local_exento = 0.00
                bien_expo_gravada = 0.00
                servicio_expo_gravada = 0.00
                bien_expo_exenta = 0.00
                servicio_expo_exento = 0.00
                iva_bien_l = 0.00
                iva_servicio_l = 0.00
                iva_bien_expo = 0.00
                iva_servicio_expo = 0.00
                total_iva = 0.00
                # amount_g = 0.00
                # amount_e = 0.00
                # amount_iva = 0.00
                tipo = "FC"
                estado = 'EMITIDA'
                cad = str(inv.name or '').split('/')
                serie = cad[0]
                numero = cad[0]
                if len(cad) > 1:
                    numero = cad[2]

                if inv.move_type == "out_refund":
                    tipo = 'NC' if inv.amount_untaxed >= 0 else 'ND'

                if inv.state == 'cancel':
                    estado = 'ANULADA'
                for line in inv.invoice_line_ids:
                    precio = line.price_unit if inv.state != 'cancel' else 0.0
                    if inv.currency_id != empresa.currency_id:
                        precio = inv.currency_id._convert(precio, empresa.currency_id, empresa, inv.invoice_date)
                    precio = precio * (1-(line.discount or 0.0)/100.0)
                    if tipo == 'NC':
                        precio = precio * -1
                    taxes = line.tax_ids.compute_all(precio, empresa.currency_id, line.quantity, line.product_id, inv.partner_id)
                    aux_gravado = taxes['total_excluded']
                    aux_iva = 0.00
                    if line.tax_ids:
                        for tax in taxes['taxes']:
                            aux_iva += tax['amount']
                    if line.product_id.tipo_gasto == "compra":
                        if line.tax_ids:
                            bien_local_gravado += aux_gravado
                            iva_bien_l += aux_iva
                            if tipo == 'NC':
                                total_nc_gravados += aux_gravado
                                total_nc_iva += aux_iva
                            elif tipo == 'ND':
                                total_nd_gravados += aux_gravado
                                total_nd_iva += aux_iva
                            else:
                                total_bienes_gravados += aux_gravado
                                total_bienes_iva += aux_iva
                        else:
                            bien_local_exento += aux_gravado
                            if tipo == 'NC':
                                total_nc_exentos += aux_gravado
                            elif tipo == 'ND':
                                total_nd_exentos += aux_gravado
                            else:
                                total_bienes_exentos += aux_gravado
                    elif line.product_id.tipo_gasto == "servicio":
                        if line.tax_ids:
                            servicio_local_gravado += aux_gravado
                            iva_servicio_l += aux_iva
                            if tipo == 'NC':
                                total_nc_gravados += aux_gravado
                                total_nc_iva += aux_iva
                            elif tipo == 'ND':
                                total_nd_gravados += aux_gravado
                                total_nd_iva += aux_iva
                            else:
                                total_serv_gravados += aux_gravado
                                total_serv_iva += aux_iva
                        else:
                            servicio_local_exento += aux_gravado
                            if tipo == 'NC':
                                total_nc_exentos += aux_gravado
                            elif tipo == 'ND':
                                total_nd_exentos += aux_gravado
                            else:
                                total_serv_exentos += aux_gravado
                    elif line.product_id.tipo_gasto == "exportacion":
                        if line.product_id.type == "service":
                            if line.tax_ids:
                                servicio_expo_gravada += aux_gravado
                                iva_servicio_expo += aux_iva
                            else:
                                servicio_expo_exento += aux_gravado
                        else:
                            if line.tax_ids:
                                bien_expo_gravada += aux_gravado
                                iva_bien_expo += aux_iva
                            else:
                                bien_expo_exenta += aux_gravado
                        if line.tax_ids:
                            if tipo == 'NC':
                                total_nc_gravados += aux_gravado
                                total_nc_iva += aux_iva
                            elif tipo == 'ND':
                                total_nd_gravados += aux_gravado
                                total_nd_iva += aux_iva
                            else:
                                total_expo_gravados += aux_gravado
                                total_expo_iva += aux_iva
                        else:
                            if tipo == 'NC':
                                total_nc_exentos += aux_gravado
                            elif tipo == 'ND':
                                total_nd_exentos += aux_gravado
                            else:
                                total_expo_exentos += aux_gravado

                total_iva = sum([iva_bien_l, iva_servicio_l, iva_bien_expo,
                                 iva_servicio_expo])
                amount_total = sum([bien_local_gravado, servicio_local_gravado,
                                    bien_local_exento, servicio_local_exento,
                                    bien_expo_gravada, servicio_expo_gravada,
                                    bien_expo_exenta, servicio_expo_exento,
                                    total_iva])
                linea = {
                    'company': empresa.name or "",
                    'estado': estado,
                    'nit': empresa.vat or "",
                    'direccion': empresa.street,
                    'folio_no': int(folio),
                    'establecimientos': establecimientos,
                    # 'mes': mes,
                    'fecha': datetime.strptime(
                        str(inv.invoice_date),
                        DEFAULT_SERVER_DATE_FORMAT).strftime(date_format),
                    'tipo': tipo,
                    'serie': serie,
                    'numero': numero,
                    'nit_cliente': inv.partner_id.vat or "C/F",
                    'cliente': inv.partner_id.name,
                    'bienes_gravados': bien_local_gravado,
                    'servicios_gravados': servicio_local_gravado,
                    'bienes_exentos': bien_local_exento,
                    'servicios_exentos': servicio_local_exento,
                    'bienes_e_gravados': bien_expo_gravada,
                    'servicios_e_gravados': servicio_expo_gravada,
                    'bienes_e_exentos': bien_expo_exenta,
                    'servicios_e_exentos': servicio_expo_exento,
                    'iva': total_iva,
                    'subtotal': amount_total,
                }
                result.append(linea)
        total_bienes = sum([total_bienes_gravados, total_bienes_exentos,
                            total_bienes_iva])
        total_servicios = sum([total_serv_gravados, total_serv_exentos,
                               total_serv_iva])
        total_nc = sum([total_nc_gravados, total_nc_exentos, total_nc_iva])
        total_nd = sum([total_nd_gravados, total_nd_exentos, total_nd_iva])
        total_gravado = sum([total_bienes_gravados, total_serv_gravados,
                             total_nc_gravados, total_nd_gravados,
                             total_expo_gravados])
        total_exento = sum([total_bienes_exentos, total_serv_exentos,
                            total_nc_exentos, total_nd_exentos,
                            total_expo_exentos])
        total_imp = sum([total_bienes_iva, total_serv_iva, total_nc_iva,
                         total_nd_iva, total_expo_iva])
        linea = {
            'cliente': "**Ultima Linea**",
            'total_bienes_gravados': total_bienes_gravados,
            'total_bienes_exentos': total_bienes_exentos,
            'total_bienes_iva': total_bienes_iva,
            'total_bienes': total_bienes,
            'total_servicios_gravados': total_serv_gravados,
            'total_servicios_exentos': total_serv_exentos,
            'total_servicios_iva': total_serv_iva,
            'total_servicios': total_servicios,
            'total_nc_gravados': total_nc_gravados,
            'total_nc_exentos': total_nc_exentos,
            'total_nc_iva': total_nc_iva,
            'total_nc': total_nc,
            'total_nd_gravados': total_nd_gravados,
            'total_nd_exentos': total_nd_exentos,
            'total_nd_iva': total_nd_iva,
            'total_nd': total_nd,
            'total_expo_gravados': total_expo_gravados,
            'total_expo_exentos': total_expo_exentos,
            'total_expo_iva': total_expo_iva,
            'total_expor': sum([total_expo_gravados, total_expo_exentos,
                                total_expo_iva]),
            'total_gravado': total_gravado,
            'total_exento': total_exento,
            'total_iva': sum([total_bienes_iva, total_serv_iva,
                              total_nc_iva, total_nd_iva, total_expo_iva]),
            'total_total': sum([total_gravado, total_exento, total_imp])
        }
        return result, linea

    #@api.multi
    def print_purchase_excel(self):
        lang_code = self.env.context.get('lang') or 'en_US'
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        for rec in self:
            if not rec.journal_ids:
                raise UserError(("No hay ningun diario seleccionado..!"))
            libro = xlwt.Workbook()
            hoja = libro.add_sheet('Libro de Compras')

            titulos_principales_style = xlwt.easyxf('borders: top_color black, bottom_color black, right_color black, left_color black,\
            left thin, right thin, top thin, bottom thin; align: horiz center; font:bold on;')
            titulos_texto_style = xlwt.easyxf('borders: top_color black, bottom_color black, right_color black, left_color black,\
            left thin, right thin, top thin, bottom thin; align: horiz left;')
            titulos_numero_style = xlwt.easyxf('borders: top_color black, bottom_color black, right_color black, left_color black,\
            left thin, right thin, top thin, bottom thin; align: horiz right;')
            company_tittle_style = xlwt.easyxf('align: horiz center; font:bold on;')
            xlwt.add_palette_colour("custom_colour", 0x21)
            libro.set_colour_RGB(0x21, 200, 200, 200)
            #Tittles Styles
            estilo = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour')
            sums_style = xlwt.easyxf('borders: top_color black, bottom_color black, right_color black, left_color black,\
            left thin, right thin, top thin, bottom thin; align: horiz right; font:bold on;')
            hoja.write_merge(0, 0, 0, 13,'LIBRO DE COMPRAS Y SERVICIOS', style=company_tittle_style)
            hoja.write_merge(1, 1, 0, 13, rec.company_id.name, style=company_tittle_style)
            hoja.write_merge(2, 2, 0, 13, (("NIT: %s") %(rec.company_id.vat)), style=company_tittle_style)
            hoja.write_merge(3, 3, 0, 13, rec.company_id.street, style=company_tittle_style)
            date_from = datetime.strptime(str(rec.date_from), DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
            date_to = datetime.strptime(str(rec.date_to), DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
            hoja.write_merge(4, 4, 0, 13, (("Del %s Al %s") %(date_from, date_to)), style=company_tittle_style)
            #Encabezados
            y = 8
            hoja.write(y, 0, 'No', style=titulos_principales_style)
            hoja.write(y, 1, 'Fecha', style=titulos_texto_style)
            hoja.write(y, 2, 'Tipo', style=titulos_texto_style)
            hoja.write(y, 3, 'Serie', style=titulos_principales_style)
            hoja.write(y, 4, 'Numero', style=titulos_principales_style)
            hoja.write(y, 5, 'NIT', style=titulos_texto_style)
            hoja.write(y, 6, 'Proveedor', style=titulos_principales_style)
            hoja.write(y, 7, 'Bienes', style=titulos_principales_style)
            hoja.write(y, 8, 'Servicios', style=titulos_principales_style)
            hoja.write(y, 9, 'Importacion', style=titulos_principales_style)
            hoja.write(y, 10, 'Compra Exenta', style=titulos_principales_style)
            hoja.write(y, 11, 'IVA', style=titulos_principales_style)
            hoja.write(y, 12, 'IDP/Otros', style=titulos_principales_style)
            hoja.write(y, 13, 'Total', style=titulos_principales_style)
            #Generate Records
            values, summary = rec.generate_records_purchase()
            item = 0
            init_rows = y
            sum_bien_gravado = sum_serv_gravado = sum_bien_i_gravado = sum_bien_exento = sum_iva = sum_idp = sum_subtotal = 0.00
            for linea in values:
                y += 1
                item += 1
                hoja.write(y, 0, item, style=titulos_texto_style)
                hoja.write(y, 1, linea['fecha'], style=titulos_texto_style)
                hoja.write(y, 2, linea['tipo'], style=titulos_texto_style)
                hoja.write(y, 3, linea['serie'], style=titulos_texto_style)
                hoja.write(y, 4, linea['numero'], style=titulos_texto_style)
                hoja.write(y, 5, linea['nit_cliente'], style=titulos_texto_style)
                hoja.write(y, 6, linea['cliente'], style=titulos_texto_style)
                hoja.write(y, 7, linea['bienes_gravados'], style=titulos_numero_style)
                hoja.write(y, 8, linea['servicios_gravados'], style=titulos_numero_style)
                hoja.write(y, 9, linea['bienes_i_gravados'], style=titulos_numero_style)
                hoja.write(y, 10, linea['bienes_exentos'], style=titulos_numero_style)
                hoja.write(y, 11, linea['iva'], style=titulos_numero_style)
                hoja.write(y, 12, linea['idp_otros'], style=titulos_numero_style)
                hoja.write(y, 13, linea['subtotal'], style=titulos_numero_style)
                sum_bien_gravado += linea['bienes_gravados']
                sum_serv_gravado += linea['servicios_gravados']
                sum_bien_i_gravado += linea['bienes_i_gravados']
                sum_bien_exento += linea['bienes_exentos']
                sum_iva += linea['iva']
                sum_idp += linea['idp_otros']
                sum_subtotal += linea['subtotal']
                
            y += 1
            #Sum on numeric cell
            hoja.write(y, 6, "*TOTALES*", style=sums_style)
            hoja.write(y, 7, xlwt.Formula((("sum(H%s:H%s)") %(init_rows, y))) , style=sums_style)
            hoja.write(y, 8, xlwt.Formula((("sum(I%s:I%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 9, xlwt.Formula((("sum(J%s:J%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 10, xlwt.Formula((("sum(K%s:K%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 11, xlwt.Formula((("sum(L%s:L%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 12, xlwt.Formula((("sum(M%s:M%s)") %(init_rows, y))), style=sums_style)
            hoja.write(y, 13, xlwt.Formula((("sum(N%s:N%s)") %(init_rows, y))), style=sums_style)
            #Summary report
            y += 3
            hoja.write(y, 6, "TOTAL BIENES", style=titulos_principales_style)
            hoja.write(y, 7, sum_bien_gravado , style=titulos_numero_style)
            y += 1
            hoja.write(y, 6, "TOTAL SERVICIOS", style=titulos_principales_style)
            hoja.write(y, 7, sum_serv_gravado, style=titulos_numero_style)
            y += 1
            hoja.write(y, 6, "TOTAL IMPORTACION", style=titulos_principales_style)
            hoja.write(y, 7, sum_bien_i_gravado, style=titulos_numero_style)
            y += 1
            hoja.write(y, 6, "TOTAL COMPRAS EXENTAS", style=titulos_principales_style)
            hoja.write(y, 7, sum_bien_exento, style=titulos_numero_style)
            y += 1
            hoja.write(y, 6, "TOTAL IVA", style=titulos_principales_style)
            hoja.write(y, 7, sum_iva, style=titulos_numero_style)
            y += 1
            hoja.write(y, 6, "TOTAL IDP/OTROS", style=titulos_principales_style)
            hoja.write(y, 7, sum_idp, style=titulos_numero_style)
            y += 1
            hoja.write(y, 6, "*TOTALES*", style=sums_style)
            hoja.write(y, 7, sum_subtotal, style=sums_style)
            #Save Excel in Wizard
            fp = BytesIO()
            libro.save(fp)
            fp.seek(0)
            report_data_file = base64.encodestring(fp.read())
            fp.close()
            self.write({'file': report_data_file})
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=wizard.ventas.compras&field=file&download=true&id=%s&filename=libro_compras.xls' % (rec.id),
            'target': 'new',
        }


    #@api.multi
    def generate_records_purchase(self):
        result = []
        tax = self.env['account.tax']
        lang_code = self.env.context.get('lang') or 'en_US'
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        tipo_doc = ""
        bienes_gravados = 0.00
        servicios_gravados = 0.00
        bienes_exentos = 0.00
        servicios_exentos = 0.00
        bienes_pc = 0.00
        servicios_pc = 0.00
        # retenciones = 0.00
        bienes_i_gravados = 0.00
        servicios_i_gravados = 0.00
        bienes_i_exentos = 0.00
        servicios_i_exentos = 0.00
        iva_bienes = 0.00
        iva_combustibles = 0.00
        iva_servicios = 0.00
        iva_impo = 0.00
        # iva_impo_s = 0.00
        # iva_impo_b = 0.00
        iva_subtotal = 0.00
        otros_impuestos = 0.00
        # idp = 0.00
        amount_g = 0.00
        amount_e = 0.00
        amount_pc = 0.00
        # amount_imp = 0.00
        amount_iva = 0.00
        subtotal = 0.00
        # total_iva = 0.00
        total_bienes_g = 0.00
        total_bienes_e = 0.00
        total_bienes_pc = 0.00
        # total_bienes = 0.00
        total_serv_g = 0.00
        total_serv_e = 0.00
        total_serv_pc = 0.00
        # total_serv= 0.00
        total_impo_g = 0.00
        total_impo_e = 0.00
        total_impo_pc = 0.00
        # total_impo = 0.00
        total_comb_g = 0.00
        total_comb_e = 0.00
        total_idp_otros = 0.00
        total_comb_pc = 0.00
        total_idp = 0.00
        # total_comb = 0.00
        fac_pc = 0
        establecimientos = ""
        mes = ""
        journal_ids = self.journal_ids.ids
        date_from = self.date_from
        date_to = self.date_to
        tax_ids = tax.search(
            ['|', ('tax_group_id', '=', self.tax_id.id),
             ('tax_group_id', '=', self.tax_id.id),
             ('type_tax_use', '=', 'purchase')]).mapped('id')
        # base_id = data['form']['base_id']
        compania = self.company_id
        #folio = data['form']['folio_inicial']
        facturas = self.env['account.move'].search(
            [('state', 'in', ['posted']),
                ('journal_id', 'in', journal_ids),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ('company_id', '=', compania.id)], order='invoice_date')
        empresa = self.env['res.company'].browse([compania.id])
        #establecimientos = ", ".join([
        #    jou.name for jou in self.env['account.journal'].browse(
        #        journal_ids)])
        # for journal in self.env['account.journal'].browse(journal_ids): 
        #     establecimientos += journal.name.encode(
        #         'ascii', 'ignore') + ", "
        for inv in facturas:
            # tipo_doc = inv.tipo_documento
            # if inv.type != 'in_invoice':
            #     tipo_doc = 'NC'
            tipo_doc = 'NC' if inv.move_type != 'in_invoice' else inv.tipo_documento
            bienes_gravados = 0.00
            servicios_gravados = 0.00
            bienes_exentos = 0.00
            idp_otros = 0.00
            total_idp_otros = 0.00
            servicios_exentos = 0.00
            bienes_pc = 0.00
            servicios_pc = 0.00
            bienes_i_gravados = 0.00
            servicios_i_gravados = 0.00
            bienes_i_exentos = 0.00
            servicios_i_exentos = 0.00
            iva_subtotal = 0.00
            # iva_subtotal_b = 0.00
            # iva_subtotal_s = 0.00
            # iva_subtotal_c = 0.00
            # iva_subtotal_i = 0.00
            otros_impuestos_b = 0.00
            otros_impuestos_s = 0.00
            retenciones_s = 0.00
            retenciones_b = 0.00
            amount_g = 0.00
            amount_e = 0.00
            amount_pc = 0.00
            # fac_pc = 0
            # amount_imp = 0.00
            amount_iva = 0.00
            # idp = 0.00
            subtotal = 0.00
            tipo_cambio = 1
            #cheque = inv.doc_origen_serie or ""
            #orden = inv.doc_origen_num or ""
            if inv.currency_id.id != inv.company_id.currency_id.id:
                total = 0
                for line in inv.line_ids:
                    if line.account_id.id:
                        total += line.credit - line.debit
                tipo_cambio = total / inv.amount_total
            estado = 'E'
            if inv.state == 'cancel':
                estado = 'A'

            if inv.tipo_documento == 'DA':
                sum_arancel = 0.0
                for tax in inv.tax_ids:
                    sum_arancel += tax.amount
                base_dua = inv.valor_base_dua or 0.0
                sum_arancel = sum_arancel * tipo_cambio

                base_dua = base_dua if estado != 'A' else 0.0
                sum_arancel = sum_arancel if estado != 'A' else 0.0

                bienes_i_gravados += base_dua
                iva_subtotal += sum_arancel
                total_impo_g += base_dua
                iva_impo += sum_arancel

                subtotal = sum([bienes_gravados, servicios_gravados,
                                bienes_exentos, servicios_exentos,
                                bienes_pc, servicios_pc, bienes_i_gravados,
                                servicios_i_gravados, bienes_i_exentos,
                                servicios_i_exentos, iva_subtotal])
                linea = {
                    'nit': empresa.vat,
                    'company': empresa.name or '',
                    'direccion': empresa.street or '',
                    'folio_no': 0,
                    'establecimientos': establecimientos,
                    'mes': mes,
                    'fecha': datetime.strptime(
                        str(inv.date),
                        DEFAULT_SERVER_DATE_FORMAT).strftime(date_format),
                    'tipo': tipo_doc,
                    'estado': estado,
                    'serie': inv.serie_factura,
                    'numero': inv.num_factura,
                    'origen': "N/A",
                    'nit_cliente': inv.partner_id.vat or "C/F",
                    'cliente': inv.partner_id.name or '',
                    'bienes_gravados': bienes_gravados,
                    'servicios_gravados': servicios_gravados,
                    'bienes_exentos': bienes_exentos,
                    'servicios_exentos': servicios_exentos,
                    'bienes_pc': bienes_pc,
                    'servicios_pc': servicios_pc,
                    'bienes_i_gravados': bienes_i_gravados,
                    'servicios_i_gravados': servicios_i_gravados,
                    'bienes_i_exentos': bienes_i_exentos,
                    'servicios_i_exentos': servicios_i_exentos,
                    'iva': iva_subtotal,
                    'subtotal': subtotal,
                }
                result.append(linea)
                continue

            for line in inv.invoice_line_ids:
                precio = (line.price_unit * (1-(
                    line.discount or 0.0)/100.0)) * tipo_cambio
                precio = precio if estado != 'A' else 0.0
                if tipo_doc == 'NC':
                    precio = precio * -1
                taxes = line.tax_ids.compute_all(
                    precio, empresa.currency_id, line.quantity,
                    line.product_id, line.partner_id)
                if line.product_id.tipo_gasto == 'compra':
                    if inv.tipo_documento == 'FPC':
                        fac_pc += 1
                        for i in taxes['taxes']:
                            if i['id'] in tax_ids:
                                bienes_pc += i['amount']
                                total_bienes_pc += i['amount']
                            elif i['amount'] > 0:
                                #otros_impuestos_b += i['amount']
                                idp_otros += i['amount']
                                total_idp_otros += i['amount']
                        bienes_pc += (taxes['total_excluded'])
                        total_bienes_pc += (taxes['total_excluded'])
                        #otros_impuestos_b = 0.00
                    else:
                        if line.tax_ids:
                            for i in taxes['taxes']:
                                if i['id'] in tax_ids:
                                    iva_subtotal += i['amount']
                                    iva_bienes += i['amount']
                                elif i['amount'] > 0:
                                    otros_impuestos_b += i['amount']
                                elif i['amount'] < 0:
                                    retenciones_b += i['amount']
                            bienes_gravados += (taxes['total_excluded'])
                            total_bienes_g += (taxes['total_excluded'])
                            #otros_impuestos_b = 0.00
                            #retenciones_b = 0.00
                        else:
                            bienes_exentos += taxes['total_excluded']
                            total_bienes_e += taxes['total_excluded']
                elif line.product_id.tipo_gasto == 'servicio':
                    if inv.tipo_documento == 'FPC':
                        fac_pc += 1
                        for i in taxes['taxes']:
                            # if all([i['base_code_id'] == base_id[0],
                            #         i['tax_code_id'] == tax_id[0]]):
                            if i['id'] in tax_ids:
                                servicios_pc += i['amount']
                                total_serv_pc += i['amount']
                            elif i['amount'] > 0:
                                otros_impuestos_s += i['amount']
                        servicios_pc += (taxes['total_excluded'])
                        total_serv_pc += (taxes['total_excluded'])
                        otros_impuestos_s = 0.00
                    else:
                        if line.tax_ids:
                            for i in taxes['taxes']:
                                # if all([i['base_code_id'] == base_id[0],
                                #         i['tax_code_id'] == tax_id[0]]):
                                if i['id'] in tax_ids:
                                    iva_subtotal += i['amount']
                                    iva_servicios += i['amount']
                                elif i['amount'] > 0:
                                    #otros_impuestos_s += i['amount']
                                    idp_otros += i['amount']
                                    total_idp_otros += i['amount']
                                elif i['amount'] < 0:
                                    retenciones_s += i['amount']
                            servicios_gravados += (taxes['total_excluded'])
                            total_serv_g += (taxes['total_excluded'])
                            #otros_impuestos_s = 0.00
                            retenciones_s = 0.00
                        else:
                            servicios_exentos += taxes['total_excluded']
                            total_serv_e += taxes['total_excluded']
                elif line.product_id.tipo_gasto == 'combustibles':
                    if inv.tipo_documento == 'FPC':
                        fac_pc += 1
                        for i in taxes['taxes']:
                            if i['id'] in tax_ids:
                                bienes_pc += i['amount']
                                total_comb_pc += i['amount']
                            elif i['amount'] > 0:
                                otros_impuestos += i['amount']
                        bienes_pc += (taxes['total_excluded'])
                        total_comb_pc += (taxes['total_excluded'])
                    else:
                        if line.tax_ids:
                            for i in taxes['taxes']:
                                if i['id'] in tax_ids:
                                    iva_subtotal += i['amount']
                                    iva_combustibles += i['amount']
                                elif i['amount'] > 0:
                                    idp_otros += i['amount']
                                    total_idp_otros += i['amount']
                                elif i['amount'] < 0:
                                    otros_impuestos += i['amount']
                            bienes_gravados += taxes['total_excluded']
                            total_comb_g += taxes['total_excluded']
                        else:
                            bienes_exentos += taxes['total_excluded']
                            total_comb_e += taxes['total_excluded']
                elif line.product_id.tipo_gasto == 'importacion':
                    if inv.tipo_documento == 'FPC':
                        fac_pc += 1
                        for i in taxes['taxes']:
                            # if all([i['base_code_id'] == base_id[0],
                            #         i['tax_code_id'] == tax_id[0]]):
                            if i['id'] in tax_ids:
                                amount_iva = i['amount']
                            # elif i['amount'] > 0:
                            #     amount_imp = i['amount']
                        amount_pc = (taxes['total_excluded'] + amount_iva)
                        amount_iva = 0.00
                    else:
                        if line.tax_ids:
                            for i in taxes['taxes']:
                                # if all([i['base_code_id'] == base_id[0],
                                #         i['tax_code_id'] == tax_id[0]]):
                                if i['id'] in tax_ids:
                                    amount_iva = i['amount']
                                # elif i['amount'] > 0:
                                #     amount_imp = i['amount']
                            amount_g = taxes['total_excluded']
                        else:
                            amount_e = taxes['total_excluded']
                    if line.product_id.type == "service":
                        if inv.tipo_documento == 'FPC':
                            servicios_pc += amount_pc
                            total_impo_pc += amount_pc
                        else:
                            if line.tax_ids:
                                servicios_i_gravados += amount_g
                                iva_subtotal += amount_iva
                                total_impo_g += amount_g
                                iva_impo += amount_iva
                            else:
                                servicios_i_exentos += amount_e
                                total_impo_e += amount_e
                    else:
                        if inv.tipo_documento == 'FPC':
                            bienes_pc += amount_pc
                            total_impo_pc += amount_pc
                        else:
                            if line.tax_ids:
                                bienes_i_gravados += amount_g
                                iva_subtotal += amount_iva
                                total_impo_g += amount_g
                                iva_impo += amount_iva
                            else:
                                bienes_i_exentos += amount_e
                                total_impo_e += amount_e

            subtotal = sum([bienes_gravados, servicios_gravados,
                            bienes_exentos, servicios_exentos,
                            bienes_pc, servicios_pc, bienes_i_gravados,
                            servicios_i_gravados, bienes_i_exentos,
                            servicios_i_exentos, iva_subtotal, idp_otros])
            linea = {
                'nit': empresa.vat,
                'company': empresa.name or '',
                'direccion': empresa.street or '',
                'folio_no': 0,
                'establecimientos': establecimientos,
                'mes': mes,
                'fecha': datetime.strptime(
                    str(inv.invoice_date),
                    DEFAULT_SERVER_DATE_FORMAT).strftime(date_format),
                'tipo': tipo_doc,
                'estado': estado,
                'serie': inv.serie_factura,
                'numero': inv.num_factura,
                'origen': "N/A",
                'nit_cliente': inv.partner_id.vat or "C/F",
                'cliente': inv.partner_id.name or '',
                'bienes_gravados': bienes_gravados,
                'servicios_gravados': servicios_gravados,
                'bienes_exentos': (bienes_exentos + servicios_exentos + bienes_pc + servicios_pc),
                #'servicios_exentos': servicios_exentos,
                #'bienes_pc': bienes_pc,
                #'servicios_pc': servicios_pc,
                'bienes_i_gravados': (bienes_i_gravados + servicios_i_gravados + bienes_i_exentos + servicios_i_exentos),
                #'servicios_i_gravados': servicios_i_gravados,
                #'bienes_i_exentos': bienes_i_exentos,
                #'servicios_i_exentos': servicios_i_exentos,
                'idp_otros': idp_otros,
                'iva': iva_subtotal,
                'subtotal': subtotal,
            }
            result.append(linea)
        total_comb = sum([total_comb_g, total_comb_e, total_comb_pc,
                          iva_combustibles])
        total_g = sum([total_bienes_g, total_comb_g, total_serv_g,
                       total_impo_g])
        total_e = sum([total_bienes_e, total_comb_e, total_serv_e,
                       total_impo_e])
        total_pc = sum([total_bienes_pc, total_comb_pc, total_serv_pc,
                        total_impo_pc])
        total_iva = sum([iva_bienes, iva_servicios, iva_impo,
                         iva_combustibles])
        total_idp = sum([total_idp_otros])
        # total_total = sum([total_g, total_e, total_pc, total_iva])
        linea = {
            'cliente': "**ULTIMA LINEA**",
            'total_bienes_g': total_bienes_g,
            'total_bienes_e': total_bienes_e,
            'total_bienes_pc': total_bienes_pc,
            'total_bienes_iva': iva_bienes,
            'total_bienes': sum([total_bienes_g, total_bienes_e,
                                 total_bienes_pc, iva_bienes]),
            'total_serv_g': total_serv_g,
            'total_serv_e': total_serv_e,
            'total_serv_pc': total_serv_pc,
            'total_serv_iva': iva_servicios,
            'total_serv': sum([total_serv_g, total_serv_e, total_serv_pc,
                               iva_servicios]),
            'total_impo_g': total_impo_g,
            'total_impo_e': total_impo_e,
            'total_impo_pc': total_impo_pc,
            'total_impo_iva': iva_impo,
            'total_impo': sum([total_impo_g, total_impo_e, total_impo_pc,
                               iva_impo]),
            'total_comb_g': total_comb_g,
            'total_comb_e': total_comb_e,
            'total_comb_pc': total_comb_pc,
            'total_comb_iva': iva_combustibles,
            'total_comb': total_comb,
            'total_g': total_g,
            'total_e': total_e,
            'total_pc': total_pc,
            'total_iva': total_iva,
            'total_total': sum([total_g, total_e, total_pc, total_iva]),
            'fac_pc': int(fac_pc),
            'fac_c': len(facturas) - fac_pc,
            'fac_total': len(facturas),
        }
        # result.append(linea)
        return result, linea

WizardVentasCompras()