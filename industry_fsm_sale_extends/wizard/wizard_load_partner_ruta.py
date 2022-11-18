# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
import base64
import tempfile
import binascii
import xlrd
from datetime import datetime,timedelta

class CargarRutas(models.TransientModel):
    _name = "wizard.cargar.rutas"
    _description = "Asistente para la carga de rutas"
    name = fields.Char(string="Nombre", default="Cargar Rutas")
    partners_file = fields.Binary(string="Clientes")
    partners_name = fields.Char(string="Nombre del archivo")

    def load_partner(self):
        if not self.partners_file:
            raise UserError(_('Debe cargar un archivo con las excepciones.'))
        contexto = self.env.context
        asignacion = self.env[contexto['active_model']].search([('id', '=', contexto['active_id'])])
        try:
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.partners_file))
            fp.seek(0)
            vals = {}
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            for i in range(sheet.nrows):
                if i == 0:
                    continue
                row = sheet.row_values(i)
                codigo = row[0]
                nombre = row[1]
                orden = row[2]
                if not codigo or not nombre or not orden:
                    continue
                partner_ids = self.env['res.partner'].search([('ref', '=', codigo), ('name', '=', nombre)])
                if partner_ids:
                    for partner_id in partner_ids:
                        asignacion.partner_ids.create({'name': partner_id.name, 'partner_id': partner_id.id, 'orden': orden, 'ruta_id': asignacion.id})          
        except Exception as e:
            raise UserError(_("Error al cargar archivo: %s") % str(e))

