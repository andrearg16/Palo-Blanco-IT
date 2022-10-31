# -*- coding: utf-8 -*-
{
    'name': "DVSISA Custom Reports",
    'author': "Xetechs GT",
    'website': "http://www.xetechs.gt",
    "version": "15.0.1.1.0",

    'depends': ['stock_landed_costs', 'stock', 'base', 'stock_account', 'purchase', 'web', 'stock_logistic_location'],
    'data': [
        'report/address_layout.xml',
        'report/destination_cost_template.xml',
        'report/purchase_order_template.xml',
        'report/purchase_quotation_template.xml',
        'report/stock_delivery_template.xml',
        'report/stock_picking_template.xml',
        'report/packing_local_label_template.xml',
        'report/reception_label_template.xml',
        'report/location_label_template.xml',
        'report/sale_remmission_template.xml',
        'report/action_report.xml',
    ]
}

