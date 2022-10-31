# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.misc import formatLang
import operator


class ReportPurchaseBook(models.AbstractModel):
    _name = 'report.report_ventas_compras.report_purchase_book'

    @api.model
    def _get_report_values(self, docids, data=None):
        company_id = data.get('form', {}).get(
            'company_id', False)
        if not company_id:
            company_id = self.env.user.company_id
        else:
            company_id = self.env['res.company'].browse(company_id[0])
            
        date = self._get_date(data)
        data, ultima = self.generate_records(data)
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'docs': docs,
            'self': self,
            'data': data,
            'ultima': ultima,
            'format_price': self._format_price,
            'company_id': company_id,
            'date': date
        }
        return docargs

    def _get_date(self, data):
        date_final = ""
        date_from = datetime.strptime(data['form']['date_from'], DEFAULT_SERVER_DATE_FORMAT).strftime("%d de %B de %Y")
        date_to = datetime.strptime(data['form']['date_to'], DEFAULT_SERVER_DATE_FORMAT).strftime("%d de %B de %Y")
        months = {'january': 'enero', 'february': 'febrero', 'march': 'marzo', 'april': 'abril', 'may': 'mayo',
                  'june': 'junio', 'july': 'julio', 'august': 'agosto', 'september': 'septiembre',
                  'november': 'noviembre', 'december': 'diciembre'}
        for k, v in months.items(): date_from = date_from.lower().replace(k, v)
        for k, v in months.items(): date_to = date_to.lower().replace(k, v)
        if date_from == date_to:
            date_final = '{}'.format(date_from).upper()
        else:
            date_final = 'Del {} al {}'.format(date_from, date_to).upper()
        return date_final

    def _format_price(self, price, currency_id):
        if not price:
            return '0.00'
        amount_f = formatLang(self.env, price, dp='Product Price',
                              currency_obj=currency_id)
        amount_f = amount_f.replace(currency_id.symbol, '').strip()
        result = amount_f.replace(',', '')
        format_final = '{0:,.2f}'.format(float(result))
        return format_final

    def generate_records(self, data):
        result = []
        if not data.get('form', False):
            return result

        tax = self.env['account.tax']
        lang_code = self.env.context.get('lang') or 'en_US'
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        tipo_doc = ""

        establecimientos = ""
        mes = ""
        journal_ids = data['form']['journal_ids']
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        tax_ids = tax.search(
            ['|', ('tax_group_id', '=', data['form']['tax_id'][0]),
             ('tax_group_id', '=', data['form']['tax_id'][0]),
             ('type_tax_use', '=', 'purchase')]).mapped('id')
        compania = data['form']['company_id']
        folio = data['form']['folio_inicial']
        facturas = self.env['account.move'].search(
            [('state', 'in', ['posted']),
                ('journal_id', 'in', journal_ids),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ('move_type', 'in', ['in_invoice', 'in_refund']),
                ('company_id', '=', compania[0])], order='invoice_date')
        empresa = self.env['res.company'].browse([compania[0]])
        establecimientos = ", ".join([
            jou.name for jou in self.env['account.journal'].browse(
                journal_ids)])
        
        # CURRENCY FROM WIZARD
        company_currency_id = self.env['res.currency'].browse(
            data['form']['currency_id'][0])

        # NUMBER OF MOVES
        no = 0

        # NUMBER OF INVOICE PER COMPANY
        final_dict = {}
        company_fac_total = {}
        company_fac_total_final = {}

        # TOTAL VALUES
        total_bienes_gravados = 0.00
        total_servicios_gravados = 0.00
        total_combustible_gravado = 0.00
        total_line_peq_contribuyente = 0.00
        total_importacion_gravada = 0.00
        total_exportacion_gravada = 0.00

        total_bienes_exento = 0.00
        total_servicios_exento = 0.00
        total_combustible_exento = 0.00
        total_line_peq_contribuyente_exento = 0.00
        total_importacion_exento = 0.00
        total_exportacion_exento = 0.00

        # TOTAL IVA PER INVOICE
        iva_bienes_gravados = 0.00
        iva_servicios_gravados = 0.00
        iva_combustible_gravado = 0.00
        iva_line_peq_contribuyente = 0.00
        iva_importacion_gravada = 0.00
        iva_exportacion_gravada = 0.00
        
        # TOTAL FINAL
        total_iva_final = 0.00
        total_idp_final = 0.00
        total_exento_final = 0.00
        total_subtotal_final = 0.00

        for inv in facturas:
            tipo_doc = 'NC' if inv.move_type == 'in_refund' or inv.move_type == 'out_refund' else inv.tipo_documento
            
            # MONTO GRAVADO
            bienes_gravados = 0.00
            servicios_gravados = 0.00
            combustible_gravado = 0.00
            line_peq_contribuyente = 0.00
            importacion_gravada = 0.00
            exportacion_gravada = 0.00

            # MONTO EXENTO
            bienes_exento = 0.00
            servicios_exento = 0.00
            combustible_exento = 0.00
            line_peq_contribuyente_exento = 0.00
            importacion_exento = 0.00
            exportacion_exento = 0.00

            # TAXES AND TOTALS 
            amount_total = 0.00
            iva_total = 0.00
            total_idp = 0.00
            total_iva_inv = 0.00 
            estado = 'E'

            # GET INVOICE NUMBER FOR EVERY PARTNER
            partner = inv.partner_id.name
            if partner in company_fac_total:
                company_fac_total[partner][0] += 1
                company_fac_total[partner][1] += ( inv.amount_total ) * (-1) if inv.move_type == 'in_refund' or inv.move_type == 'out_refund' else inv.amount_total
            else:
                company_fac_total[partner] = [1, ( inv.amount_total ) * (-1) if inv.move_type == 'in_refund' or inv.move_type == 'out_refund' else inv.amount_total, inv.partner_id.vat or "C/F"]

            if inv.state == 'cancel':
                estado = 'A'

            for line in inv.invoice_line_ids:
                prices = ""
                idp_line = 0.00
                iva_line = 0.00
                total_price_line = 0.00
                tax_line_total = 0.00
                price_total = 0.00

                move_name = inv.name
                fel_serie = inv.serie_factura if inv.tipo_documento != 'FE' else inv.fel_serie
                fel_no = inv.num_factura if inv.tipo_documento != 'FE' else inv.fel_no
                
                if inv.journal_id.is_factura_especial == True:
                    precio = (line.quantity * line.price_unit) if inv.state != 'cancel' else 0.0
                else:
                    precio = line.price_total if inv.state != 'cancel' else 0.0
                if inv.currency_id != empresa.currency_id:
                    precio = inv.currency_id._convert(precio, empresa.currency_id, empresa, inv.invoice_date)

                precio = precio if estado != 'A' else 0.0
                if tipo_doc == 'NC':
                    precio = precio * -1

                # GET PRICES 
                total_price_line += line.price_subtotal if inv.currency_id == company_currency_id else line.amount_currency_final 

                # GET TAXES 
                taxes = line.tax_ids.compute_all(
                    line.price_unit, empresa.currency_id, line.quantity,
                    line.product_id, inv.partner_id)

                for tax in taxes['taxes']:
                    if 'IDP' in tax['name']:
                        idp_line = tax['amount'] if inv.currency_id == company_currency_id else line.idp_currency_final
                        total_idp += idp_line if inv.currency_id == company_currency_id else line.idp_currency_final
                    if 'IVA' in tax['name']:
                        iva_line = tax['amount'] if inv.currency_id == company_currency_id else line.iva_currency_final
                        total_iva_inv += iva_line if inv.currency_id == company_currency_id else line.iva_currency_final

                tax_line_total = idp_line + iva_line

                # GET AMOUNT UNTAXED AND PRICE TOTAL WITH TAXES
                if inv.move_type == 'in_refund' or inv.move_type == 'out_refund':
                    amount_untaxed = ( inv.amount_untaxed ) * (-1) if inv.currency_id == company_currency_id else ( inv.amount_untaxed_signed ) * (-1)
                    price_total = ( total_price_line ) * (-1)
                    total_iva_inv = total_iva_inv * (-1)
                    total_idp = total_idp * (-1)
                else:
                    amount_untaxed = inv.amount_untaxed if inv.currency_id == company_currency_id else inv.amount_untaxed_signed
                    price_total = total_price_line

                # GET VALUES OF LINES 
                if line.expense_type_xt == 'compra':
                    if not tax_line_total == 0:
                        bienes_gravados += price_total
                        iva_bienes_gravados += iva_line
                    else:
                        bienes_exento += price_total

                if line.expense_type_xt == 'servicio':
                    if not tax_line_total == 0:
                        servicios_gravados += price_total
                        iva_servicios_gravados += iva_line
                    else:
                        servicios_exento += price_total

                if line.expense_type_xt == 'combustibles':
                    if not tax_line_total == 0:
                        combustible_gravado += price_total
                        iva_combustible_gravado += iva_line
                    else:
                        combustible_exento += price_total

                if line.expense_type_xt == 'importacion':
                    if not tax_line_total == 0:
                        importacion_gravada += price_total
                        iva_importacion_gravada += iva_line
                    else:
                        importacion_exento += price_total

                if line.expense_type_xt == 'exportacion':
                    if not tax_line_total == 0:
                        exportacion_gravada += price_total
                        iva_exportacion_gravada += iva_line
                    else:
                        exportacion_exento += price_total

                if line.expense_type_xt == 'peqcontribuyente':
                    if not tax_line_total == 0:
                        line_peq_contribuyente += price_total
                        iva_line_peq_contribuyente += iva_line
                    else:
                        line_peq_contribuyente_exento += price_total

            # IVA, NUMBER AND AMOUNT TOTAL
            no += 1
            if inv.move_type == 'in_refund' or inv.move_type == 'out_refund':
                amount_total = ( inv.amount_tax + inv.amount_untaxed ) * (-1) if inv.currency_id == company_currency_id else ( inv.amount_tax_signed + inv.amount_untaxed_signed ) * (-1)
            else:
                amount_total = inv.amount_tax + inv.amount_untaxed if inv.currency_id == company_currency_id else inv.amount_tax_signed + inv.amount_untaxed_signed
            iva_total = amount_total - amount_untaxed - total_idp

            # SUM TOTAL VALUES 
            total_bienes_gravados += bienes_gravados
            total_servicios_gravados += servicios_gravados
            total_combustible_gravado += combustible_gravado
            total_line_peq_contribuyente += line_peq_contribuyente
            total_importacion_gravada += importacion_gravada
            total_exportacion_gravada += exportacion_gravada

            total_bienes_exento += bienes_exento
            total_servicios_exento += servicios_exento
            total_combustible_exento += combustible_exento
            total_line_peq_contribuyente_exento += line_peq_contribuyente_exento
            total_importacion_exento += importacion_exento
            total_exportacion_exento += exportacion_exento

            # TOTAL FINAL
            total_iva_final += iva_total
            total_idp_final += total_idp
            total_exento_final += price_total if tax_line_total == 0 else 0.00
            total_subtotal_final += amount_total if inv.currency_id == company_currency_id else inv.amount_total_signed

            linea = {
                'no': no,
                'nit': empresa.vat,
                'company': empresa.name.encode('ascii', 'ignore') or '',
                'direccion': empresa.street.encode(
                    'ascii', 'ignore') or '',
                'folio_no': int(folio),
                'establecimientos': establecimientos,
                'mes': mes,
                'fecha': datetime.strptime(
                    str(inv.invoice_date),
                    DEFAULT_SERVER_DATE_FORMAT).strftime(date_format),
                'tipo': tipo_doc,
                'estado': estado,
                'move_name': move_name,
                'serie': fel_serie,
                'numero': fel_no,
                'origen': "N/A",
                'nit_cliente': inv.partner_id.vat or "C/F",
                'cliente': inv.partner_id.name or '',

                'bienes_gravados': bienes_gravados,
                'servicios_gravados': servicios_gravados,
                'importacion_gravada': importacion_gravada,
                'exportacion_gravada': exportacion_gravada,
                'combustible_gravado': combustible_gravado,
                'peq_contribuyente': line_peq_contribuyente,

                'bienes_exento': bienes_exento,
                'servicios_exento': servicios_exento,
                'combustible_exento': combustible_exento,
                'line_peq_contribuyente_exento': line_peq_contribuyente_exento,
                'importacion_exento': importacion_exento,
                'exportacion_exento': exportacion_exento,

                'iva': iva_total,
                'idp': total_idp,
                'subtotal': amount_total if inv.currency_id == company_currency_id else inv.amount_total_signed,
            }

            result.append(linea)

        # ORDER DICT WITH MOVE AMOUNT
        for dict_item in company_fac_total:
            company_fac_total_final[dict_item] = company_fac_total[dict_item][1]

        partner_sort = sorted(company_fac_total_final.items(), key=operator.itemgetter(1), reverse=True)
        
        for partner in enumerate(partner_sort):
            final_dict[partner[1][0]] = company_fac_total[partner[1][0]]

        # TOTALS 
        linea = {
            'cliente': "**ULTIMA LINEA**",
            'company_fac_total': final_dict,
            'total_bienes_gravados': total_bienes_gravados,
            'total_servicios_gravados': total_servicios_gravados,
            'total_combustible_gravado': total_combustible_gravado,
            'total_line_peq_contribuyente': total_line_peq_contribuyente,
            'total_importacion_gravada': total_importacion_gravada,
            'total_exportacion_gravada': total_exportacion_gravada,

            'total_bienes_exento': total_bienes_exento,
            'total_servicios_exento': total_servicios_exento,
            'total_combustible_exento': total_combustible_exento,
            'total_line_peq_contribuyente_exento': total_line_peq_contribuyente_exento,
            'total_importacion_exento': total_importacion_exento,
            'total_exportacion_exento': total_exportacion_exento,
            
            'iva_bienes_gravados': iva_bienes_gravados,
            'iva_servicios_gravados': iva_servicios_gravados,
            'iva_combustible_gravado': iva_combustible_gravado,
            'iva_line_peq_contribuyente': iva_line_peq_contribuyente,
            'iva_importacion_gravada': iva_importacion_gravada,
            'iva_exportacion_gravada': iva_exportacion_gravada,

            'subtotal_bienes': total_bienes_gravados + total_bienes_exento + iva_bienes_gravados,
            'subtotal_servicios': total_servicios_gravados + total_bienes_exento + iva_servicios_gravados,
            'subtotal_combustible': total_combustible_gravado + total_combustible_exento + iva_combustible_gravado,
            'subtotal_line_peq_contribuyente': total_line_peq_contribuyente + total_line_peq_contribuyente_exento + iva_line_peq_contribuyente,
            'subtotal_importacion': total_importacion_gravada + total_importacion_exento + iva_importacion_gravada,
            'subtotal_exportacion': total_exportacion_gravada + total_exportacion_exento + iva_exportacion_gravada,

            'total_iva_final': total_iva_final,
            'total_idp_final': total_idp_final,
            'total_exento_final': total_exento_final,
            'total_subtotal_final': total_subtotal_final,

            'total_no_fac': no,
        }

        # split in folios
        results = []
        folio = 1
        i = 1
        rows = []
        for row in result:
            rows.append(row)
            if i == 20:
                results.append([folio, rows])
                rows = []
                i = 1
                folio += 1
            else:
                i += 1
        if len(rows) > 0:
            results.append([folio, rows])
        return results, linea
