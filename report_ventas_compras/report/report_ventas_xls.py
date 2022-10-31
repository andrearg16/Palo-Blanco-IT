# -*- encoding: utf-8 -*-

import time, datetime

from odoo import fields, models, api
from datetime import datetime, date
import base64
import io
import time

MONTHS = {
    'January': 'Enero', 
    'February': 'Febrero', 
    'March': 'Marzo', 
    'April': 'Abril', 
    'May': 'Mayo',
    'June': 'Junio', 
    'July': 'Julio', 
    'August': 'Agosto', 
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre', 
    'December': 'Diciembre'
}

class ReportSaleBookXlsx(models.AbstractModel):
    _name = 'report.report_ventas_compras.report_sale_book_xls'
    _inherit = ['report.report_xlsx.abstract', 'report.report_ventas_compras.report_sale_book']

    def _get_format_date(self, date):
        B = MONTHS[ date.strftime('%B') ]
        return date.strftime('%d de '+ B + ' del %Y')

    def generate_xlsx_report(self, workbook, docids, data):
        report_name = "new"
        row = 9
        column = 1
        total_final = 0
        now = datetime.now()
        time_now = now.strftime("%Y/%m/%d %H:%M:%S")

        # SHEET AND STYLES 
        sheet = workbook.add_worksheet("Purchase Book")
        title = workbook.add_format({'font_size': 20, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        title_no_border = workbook.add_format({'font_size': 16, 'bold': True, 'valign': 'vcenter'})
        date = workbook.add_format({'font_size': 12, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        bold = workbook.add_format({'font_size': 12, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,})
        no_bold = workbook.add_format({'font_size': 12, 'bold': False, 'valign': 'vcenter', 'border': 1,})
        no_bold_no_border = workbook.add_format({'font_size': 12, 'bold': False, 'valign': 'vcenter'})
        no_bold_no = workbook.add_format({'font_size': 12, 'bold': False, 'align': 'center', 'valign': 'vcenter', 'border': 1,})
        no_bold_number = workbook.add_format({'font_size': 12, 'bold': False, 'align': 'right', 'valign': 'vcenter', 'border': 1,})
        no_bold_total = workbook.add_format({'font_size': 12, 'bold': False, 'align': 'right', 'valign': 'vcenter', 'border': 1,})
        total = workbook.add_format({'font_size': 12, 'bold': True, 'align': 'right', 'valign': 'vcenter', 'border': 1,})
        total_table = workbook.add_format({'font_size': 12, 'bold': True, 'valign': 'vcenter', 'border': 1,})
        total_table_center = workbook.add_format({'font_size': 12, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,})
        total_amount_table = workbook.add_format({'font_size': 12, 'bold': True, 'align': 'right', 'valign': 'vcenter', 'border': 1,})

        # SET DINAMIC HEIGHT OF COLUMNS
        bold.set_text_wrap()

        # GET VALUES 
        lineas, ultima = self.generate_records(docids)
        if data.date_from == data.date_to:
            fecha = self._get_format_date(data.date_from)
        else:
            fecha = 'Del ' + self._get_format_date(data.date_from) + ' al ' + self._get_format_date(data.date_to)
        company_street = data.company_id.street if data.company_id.street else ""
        company_street2 = data.company_id.street2 if data.company_id.street2 else ""
        company_city = data.company_id.city if data.company_id.city else ""
        company_state_id = data.company_id.state_id.name if data.company_id.state_id else ""
        company_zip = data.company_id.zip if data.company_id.zip else ""
        company_country_id = data.company_id.country_id.name if data.company_id.country_id else ""
        company_vat = data.company_id.vat if data.company_id.vat else ""
        company_phone = data.company_id.phone if data.company_id.phone else ""

        # SIZE OF COLUMNS
        # WIDTH  
        sheet.set_column('B:B', 8)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 20)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 50)
        sheet.set_column('J:J', 20)
        sheet.set_column('K:K', 20)
        sheet.set_column('L:L', 20)
        sheet.set_column('M:M', 20)
        sheet.set_column('N:N', 20)
        sheet.set_column('O:O', 20)

        # HEIGTH 
        sheet.set_row(9, 20)
        sheet.set_row(10, 20)

        # SET HEADER 
        sheet.merge_range('E2:O2', data.company_id.name, title_no_border)
        sheet.merge_range('E3:O3', company_street + ", " + company_street2, no_bold_no_border)
        sheet.merge_range('E4:O4', company_city + " " + company_state_id + " " + company_zip + ", " + company_country_id, no_bold_no_border)
        sheet.merge_range('E5:O5', "NIT: " + company_vat, no_bold_no_border)
        sheet.merge_range('E6:O6', "Tel:" + company_phone, no_bold_no_border)
        
        sheet.merge_range('B8:O8', 'LIBRO DE VENTAS', title)
        sheet.merge_range('B9:O9', fecha, date)
        
        # IMAGE LOGO 
        if data.company_id.logo:
            company_logo = io.BytesIO(base64.b64decode(data.company_id.logo))
            sheet.insert_image('B2', "image.png", {'image_data': company_logo, 'x_scale': 0.27, 'y_scale': 0.21})

        # SET MENU 
        sheet.merge_range('B10:B11', 'No.', bold)
        sheet.merge_range('C10:C11', 'FECHA', bold)
        sheet.merge_range('D10:D11', 'DOC.', bold)
        sheet.merge_range('E10:E11', 'NO. INTERNO', bold)
        sheet.merge_range('F10:F11', 'SERIE', bold)
        sheet.merge_range('G10:G11', 'NO.', bold)
        sheet.merge_range('H10:H11', 'NIT', bold)
        sheet.merge_range('I10:I11', 'NOMBRE DEL CLIENTE', bold)
        sheet.merge_range('J10:K10', 'BASE GRAVADA', bold)
        sheet.merge_range('L10:M10', 'BASE EXENTA', bold)
        sheet.write('J11', 'BIENES', bold)
        sheet.write('K11', 'SERVICIOS', bold)
        sheet.write('L11', 'BIENES', bold)
        sheet.write('M11', 'SERVICIOS', bold)
        sheet.merge_range('N10:N11', 'IVA', bold)
        sheet.merge_range('O10:O11', 'MONTO IVA INCLUIDO', bold)

        # SET LINES 
        for linea in lineas: 
            for line in linea[1]:
                sheet.write(row+2, column, line['no'], no_bold_no)
                sheet.write(row+2, column+1, line['fecha'], no_bold_no)
                sheet.write(row+2, column+2, line['tipo'], no_bold)
                sheet.write(row+2, column+3, line['move_name'], no_bold_no)
                sheet.write(row+2, column+4, line['serie'], no_bold_no)
                sheet.write(row+2, column+5, line['numero'], no_bold_no)
                sheet.write(row+2, column+6, line['nit_cliente'], no_bold_no)
                sheet.write(row+2, column+7, line['cliente'], no_bold_no)
                sheet.write(row+2, column+8, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(line['bienes_gravados']), no_bold_number)
                sheet.write(row+2, column+9, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(line['servicios_gravados']), no_bold_number)
                sheet.write(row+2, column+10, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(line['bienes_exentos']), no_bold_number)
                sheet.write(row+2, column+11, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(line['servicios_exentos']), no_bold_number)
                sheet.write(row+2, column+12, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(line['iva']), no_bold_number)
                sheet.write(row+2, column+13, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(line['subtotal']), no_bold_number)

                row += 1

        # SET TOTALS
        linea_total = 'B'+str(row+3)+':I'+str(row+3)
        sheet.merge_range(linea_total, 'TOTALES', total)

        sheet.write(row+2, column+8, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_bienes_gravados']), total)
        sheet.write(row+2, column+9, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_servicios_gravados']), total)
        sheet.write(row+2, column+10, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_bienes_exentos']), total)
        sheet.write(row+2, column+11, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_servicios_exentos']), total)
        sheet.write(row+2, column+12, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_iva_final']), total)
        sheet.write(row+2, column+13, data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_subtotal_final']), total)
        
        # TABLE INVOICE TOTALS
        sheet.merge_range('B'+str(row+6)+':E'+str(row+6), 'TOTALES POR FACTURAS', total_table_center)
        sheet.merge_range('B'+str(row+7)+':D'+str(row+7), 'TOTAL BIENES GRAVADOS', total_table)
        sheet.merge_range('B'+str(row+8)+':D'+str(row+8), 'TOTAL BIENES EXENTOS', total_table)
        sheet.merge_range('B'+str(row+9)+':D'+str(row+9), 'TOTAL SERVICIOS GRAVADOS', total_table)
        sheet.merge_range('B'+str(row+10)+':D'+str(row+10), 'TOTAL SERVICIOS EXENTOS', total_table)
        sheet.merge_range('B'+str(row+11)+':D'+str(row+11), 'TOTAL IVA', total_table)
        sheet.merge_range('B'+str(row+12)+':D'+str(row+12), '**TOTAL**', total_table)
        
        sheet.write('E'+str(row+7), data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_bienes_gravados']), total_amount_table)
        sheet.write('E'+str(row+8), data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_bienes_exentos']), total_amount_table)
        sheet.write('E'+str(row+9), data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_servicios_gravados']), total_amount_table)
        sheet.write('E'+str(row+10), data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_servicios_exentos']), total_amount_table)
        sheet.write('E'+str(row+11), data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_iva_final']), total_amount_table)
        sheet.write('E'+str(row+12), data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_subtotal_final']), total_amount_table)
        
        # TABLE PARTNER TOTALS
        sheet.merge_range('H'+str(row+6)+':L'+str(row+6), 'TOTALES POR CLIENTES', total_table_center)
        sheet.write('H'+str(row+7), 'NO.', total_table_center)
        sheet.write('I'+str(row+7), 'CLIENTE', total_table_center)
        sheet.write('J'+str(row+7), 'NIT', total_table_center)
        sheet.write('K'+str(row+7), 'NUM. DE FACTURAS', total_table_center)
        sheet.write('L'+str(row+7), 'TOTAL DE FACTURAS', total_table_center)
        
        line_number = 1
        
        for total_fac in ultima['company_fac_total']: 
            sheet.write('H'+str(row+8), line_number, total_table_center)
            sheet.write('I'+str(row+8), total_fac, total_table_center)
            sheet.write('J'+str(row+8), ultima['company_fac_total'].get(total_fac)[2], total_table_center)
            sheet.write('K'+str(row+8), ultima['company_fac_total'].get(total_fac)[0], total_table_center)
            sheet.write('L'+str(row+8), data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['company_fac_total'].get(total_fac)[1]), total_table_center)
            
            row += 1
            line_number += 1
        
        sheet.write('H'+str(row+8), '', total_table_center)
        sheet.write('I'+str(row+8), '', total_table_center)
        sheet.write('J'+str(row+8), '**TOTAL**', total_table_center)
        sheet.write('K'+str(row+8), ultima['total_no_fac'], total_table_center)
        sheet.write('L'+str(row+8), data.company_id.currency_id.symbol + '. ' + '{0:,.2f}'.format(ultima['total_subtotal_final'],), total_table_center)