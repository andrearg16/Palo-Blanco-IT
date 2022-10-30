# -*- coding: utf-8 -*-
{
    'name': "customproduct",

    'summary': """
        Custom module for product""",

    'description': """
        Custom module for product
    """,

    'author': "Miguel Fuentes",
    'website': "https://www.xetechs.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase', 'stock'],

    # always loaded
    'data': [
        'views/product_inherit_view.xml',
    ],
}
