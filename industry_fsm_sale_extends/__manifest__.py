# -*- coding: utf-8 -*-
{
    'name': "industry_fsm_sale_extends",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['base','industry_fsm_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/gestion_rutas_views.xml',
        #'views/templates.xml',
        'views/rutas_views.xml',
        'views/res_partner_views.xml',
        'views/account_payment.xml',
        'views/account_move.xml',
        'wizard/wizard_load_partner_ruta_views.xml',
        'report/report_ticket_payment.xml',
        'views/account_move_homeworks.xml',    
        ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
