# -*- coding: utf-8 -*-

{
    'name': 'Account Invoice FEL -MEGAPRINT',
    'version': '1.0.1',
    'author': 'Xetechs, S.A.',
    'website': 'https://www.xetechs.com', 
    'support': 'Luis Aquino --> laquino@xetechs.com', 
    'category': 'Accounting',
    'depends': ['account', 'sale', 'report_ventas_compras'],
    'summary': 'Transfer Invoice To MegaPrint And Receive Certificate',
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/account_invoice.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/satdte_frases.xml',
        'views/account_journal_views.xml',
        'views/satdte_frases_data.xml',
        'wizard/wizard_cancel_view.xml',
        'report/invoice_megaprint_template.xml',
        'report/action_report.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
