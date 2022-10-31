# -*- encoding: UTF-8 -*-
##############################################################################
from odoo import fields, models, api, _

class ProductTemplate(models.Model):
	_inherit = "product.template"
	
	expense_type_xt = fields.Selection([('compra', 'Bienes'), ('servicio', 'Servicios'), ('combustibles', 'Combustibles/Lubricantes'), ('importacion', 'Importaciones'), ('exportacion', 'Exportaciones'), ('peqcontribuyente', 'Pequeño Contribuyente'), ('n/a', 'N/A')],'Tipo Gasto', default='compra', required=True, store=True, help="Tipo de gasto que se reflejara en el libro de Ventas/Compras del IVA")

	list_price = fields.Float(
        'Sales Price', default=1.0,
        digits='Product Price', company_dependent=True, 
        help="Price at which the product is sold to customers.",
    )
	