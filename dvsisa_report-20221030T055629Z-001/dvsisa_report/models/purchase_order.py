# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

try:
    from num2words import num2words
except:
    raise UserError(_("run Command: 'pip install num2words'"))
    
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # GET AMOUNT IN WORDS
    def get_num2words(self, amount, currency):
        final_number = ""
        final_decimal = ""
        
        final_amount = '{:.2f}'.format(amount)
        point = final_amount.find('.')
        
        number = num2words(float(final_amount[0:point]), lang='es', to='currency') 
        decimal = num2words(float(final_amount[point+1:point+3]), lang='es', to='currency') 
        
        if 'euros' in number:
            if currency == 'USD':
                final_number = number.replace("euros", "Dólares")
            else:
                final_number = number.replace("euros", "Quetzales")
        else:
            if currency == 'USD':
                final_number = number.replace("euro", "Dólar")
            else:
                final_number = number.replace("euro", "Quetzal")
        
        if 'euros' in decimal:
            final_decimal = decimal.replace("euros", "Centavos")
        
        if final_decimal:
            result = final_number + " con " + final_decimal
        else:
            if 'Quetzales' in final_number:
                result = final_number + " Exactos"
            else:
                result = final_number + " Exacto"
            
        return result
    