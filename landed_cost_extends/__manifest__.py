# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019 Xetechs, S.A. (<https://www.xetechs.com>).
#
#    For Module Support : laquino@xetechs.com --> Luis Aquino + 502 4814-3481
#
##############################################################################

{
    'name': 'Odoo Landed cost on Average Costing -Extends-',
    'version': '1.0',
    'sequence': 1,
    'category': 'Generic Modules/Warehouse',
    'license': 'LGPL-3',
    'summary': 'odoo Apps will calculate average costing on landed Cost',
    'description': """
odoo module will calculate average cost on landed costing
        
        
        odoo landed cost 
        odoo Average costing on landed cost 
        odoo landed cost with Average costing
       
        
        
    """,
    'depends': ['stock_landed_costs', 'dev_landed_cost_average_price'],
    'data': [
        'security/groups_security.xml',
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/stock_picking_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    'author': 'Luis Aquino --> laquino@xetechs.com',
    'website': 'https://xetechs.odoo.com',    
    'maintainer': 'Xetechs, S.A.', 
    'support': 'laquino@xetechs.com',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
