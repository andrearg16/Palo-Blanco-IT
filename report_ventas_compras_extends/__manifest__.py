# -*- encoding: UTF-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2018-Today XETECHS, S.A.
#    (<https://xetechs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
	'name': 'Libro de Ventas/Compras -Excel-',
	'summary': """Libro de Ventas/Compras -Excel-""",
	'version': '1.0.',
	'description': """El modulo imprime el libro de Ventas/Compras para declaracion del IVA""",
	'author': 'XETECHS, S.A.',
	'maintainer': 'XETECHS, S.A.',
	'website': 'https://www.xetechs.com',
	'category': 'account',
	'depends': ['report_ventas_compras'],
	'license': 'AGPL-3',
	'data': [
		'wizard/wizard_ventas_compras_view.xml',
	],
	'demo': [],
	'installable': True,
	'auto_install': False,
}
