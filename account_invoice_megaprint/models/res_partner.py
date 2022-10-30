# -*- coding: utf-8 -*-

from odoo import api, fields, models
import requests
import json
import dateutil.parser
from odoo.exceptions import UserError
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, fromstring
from xml.dom import minidom

class ResPartner(models.Model):
    _inherit = "res.partner"

    type_document = fields.Selection([('CUI', 'Con DPI'), ('EXT', 'Con Pasaporte'), ('NIT', 'Con NIT')], string="Documento", default="NIT")

    @api.onchange('vat')
    def onchange_nit(self):
        if self.vat:
            nit = self.vat
            if '-' in nit:
                self.vat = nit.replace('-', '')
