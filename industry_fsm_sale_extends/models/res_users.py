# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResUsers(models.Model):

    _inherit = "res.users"

    rutas_ids = fields.One2many('rutas', 'user_id', string='Rutas')