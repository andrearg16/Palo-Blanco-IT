# -*- encoding: UTF-8 -*-

{
	'name': 'Reporte de Ventas y Compras',
	'summary': """Reporte de Ventas y Compras para Guatemala""",
	'version': '1.0.',
	'description': """Permite Generar Reporte de Ventas y Compras de IVA""",
	'author': 'Luis Aquino --> laquino@xetechs.com / Jonathan Quintero --> jquintero@xetechs.com',
	'maintainer': 'Xetechs, S.A.',
	'website': 'https://www.xetechs.odoo.com',
	'category': 'account',
	'depends': ['account', 'account_reports', 'report_xlsx', 'product'],
	'license': 'AGPL-3',
	'data': [
		'security/groups.xml',
		"security/ir.model.access.csv",
		'views/account_move_view.xml',
		'views/product_template_view.xml',
		'report/report_purchase_book_template.xml',
		'report/report_sale_book_template.xml',
        'report/ab_reports.xml',
		'wizard/wizard_ventas_compras_view.xml',
	],
	"assets": {
        "web.assets_backend": [
            "/report_ventas_compras/static/src/css/invoice.css",
        ],
    },
	'demo': [],
	'installable': True,
	'auto_install': False,
}
