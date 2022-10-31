# -*- encoding: UTF-8 -*-
##############################################################################

from odoo import fields, models, api, _
import logging

_logger = logging.getLogger( __name__ )


class AccountMove(models.Model):
	_inherit = "account.move"
	
	serie_factura = fields.Char(string="Serie Factura", required=False, help="Serie de la factura de proveedor")
	num_factura = fields.Char(string="Numero Factura", required=False, help="Numero de la factura de proveedor")
	tipo_documento = fields.Selection(string="Tipo Documento", selection='_get_tipo_documento', default='FC', required=True, help="Tipo de documento de gasto que se reflejara en el libro de Ventas/Compras del IVA")

	def _get_tipo_documento(self):
		if self.env.company.name == 'American Telecommunications S.A.':
			selection = [
				('FC', 'Factura Cambiaria'),
				('FE', 'Factura Especial'),
				('FCE', 'Factura Electronica'),
						('FAC', 'Factura'),
						('FEL', 'FEL'),
				('NC', 'Nota de Credito'),
				('ND', 'Nota de Debito'),
				('FPC', 'Factura Peq. Contribuyente'),
				('DA', 'Declaracion Unica Aduanera'),
				('FA', 'FAUCA'),
				('FO', 'Formulario SAT'),
                ('ONAF', 'Otros No Afectos'),
                ('EP', 'Escritura Publica'),
			]
		else: 
			selection = [
				('FC', 'Factura Cambiaria'),
				('FE', 'Factura Especial'),
				('FCE', 'Factura Electronica'),
				('FAC', 'Factura'),
				('FEL', 'FEL'),
				('NC', 'Nota de Credito'),
				('ND', 'Nota de Debito'),
				('FPC', 'Factura Peq. Contribuyente'),
				('DA', 'Declaracion Unica Aduanera'),
				('FA', 'FAUCA'),
				('FO', 'Formulario SAT'),
				('ONAF', 'Otros No Afectos'),
				('EP', 'Escritura Publica'),
				('DU', 'DUCA'),
				('REC', 'Recibo'),
				('CCF', 'CCF'),
				('FAEX', 'FAEX'),
				('TICKET', 'TICKET'),
			]
		return selection


class AccountMoveLine(models.Model):
	_inherit = "account.move.line"

	expense_type_xt = fields.Selection(string="Tipo Gasto", store=True, selection='_get_expense_type_xt', default='compra', required=True, help="Tipo de gasto que se reflejara en el libro de Ventas/Compras del IVA")
    
	# FIELDS TO SAVE THE MULTI_CURRENCY
	amount_currency_final = fields.Monetary(string='Total en Moneda de la Compañia', store=True, readonly=True, tracking=True, compute='_compute_currency_fields', currency_field="company_currency_id")
	iva_currency_final = fields.Monetary(string='Total IVA en Moneda de la Compañia', store=True, readonly=True, tracking=True, compute='_compute_currency_fields', currency_field="company_currency_id")
	idp_currency_final = fields.Monetary(string='Total IDP en Moneda de la Compañia', store=True, readonly=True, tracking=True, compute='_compute_currency_fields', currency_field="company_currency_id")
	
	
	@api.depends('price_subtotal')
	def _compute_currency_fields(self):
		for line in self:
			amount_currency_final = 0.00
			iva_currency_final = 0.00
			idp_currency_final = 0.00
			
			if line.price_subtotal:
				amount_currency_final = line.currency_id._convert(line.price_subtotal, line.company_id.currency_id, line.company_id, line.date)
				
			taxes = line.tax_ids.compute_all(
				line.price_unit, line.currency_id, line.quantity,
				line.product_id, line.partner_id)
			
			if taxes:
				for tax in taxes['taxes']:
					if 'IDP' in tax['name']:
						idp_currency_final = line.currency_id._convert(tax['amount'], line.company_id.currency_id, line.company_id, line.date)
					if 'IVA' in tax['name']:
						iva_currency_final = line.currency_id._convert(tax['amount'], line.company_id.currency_id, line.company_id, line.date)
				
			line.amount_currency_final = amount_currency_final
			line.iva_currency_final = iva_currency_final
			line.idp_currency_final = idp_currency_final

	def _get_expense_type_xt(self):
		if self._context.get('default_move_type') and self._context.get('default_move_type') == 'out_invoice':
			selection = [
				('compra', 'Bienes'), 
				('servicio', 'Servicios'), 
				('n/a', 'N/A')
			]
		else: 
			selection = [
				('compra', 'Bienes'), 
				('servicio', 'Servicios'), 
				('importacion', 'Importaciones'), 
				('peqcontribuyente', 'Pequeño Contribuyente'), 
				('n/a', 'N/A')
			]
		return selection  
        
	@api.onchange('product_id.expense_type_xt', 'product_id')
	def _onchange_expense_type_related(self):
		for order in self:
			order.expense_type_xt = order.product_id.expense_type_xt if order.product_id.expense_type_xt else ""
