# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Rutas(models.Model):
    _name = 'rutas'
    _description = 'rutas.rutas'

    name = fields.Char(string='Nombre', required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    active = fields.Boolean(default=True)
    state_id = fields.Many2one('res.country.state', string='Departamento',
        help="Departamentos")
    user_id = fields.Many2one('res.users', string='Vendedor')
    partner_ids = fields.One2many('asignacion.vendedor.ruta', 'ruta_id' ,string='Clientes')
    country_id = fields.Many2one('res.country', related='company_id.country_id')

    @api.onchange("company_id")
    def _onchange_company_id(self):
        for rec in self:
            return {"domain":{"state_id":[("country_id","=", rec.country_id.id)]}}
    
    def unlink(self):
        for record in self:
            if record.partner_ids:
                record.partner_ids.unlink()
        super(Rutas, self).unlink()

    def load_partner(self):
        new_wizard = self.env['wizard.cargar.rutas'].create({'name': 'Carga masiva'})
        view_id = self.env.ref('industry_fsm_sale_extends.wizard_carga_masiva_clientes').id

        return {
            'type': 'ir.actions.act_window',
            'name': _('Carga de Clientes'),
            'view_mode': 'form',
            'res_model': 'wizard.cargar.rutas',
            'target': 'new',
            'res_id': new_wizard.id,
            'views': [[view_id, 'form']],
        }

class AsignacionVendedorRuta(models.Model):
    _name = 'asignacion.vendedor.ruta'
    _description = 'Asignacion vendedor ruta'
    _order = "orden asc"

    name = fields.Char(string='Nombre', required=True, default='Asignacion vendedor ruta')
    orden = fields.Integer(string='Orden de visita', required=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    ruta_id = fields.Many2one('rutas', string='Ruta')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)



class PlanificadorRutas(models.Model):
    _name = 'planificador.rutas'
    _description = 'Planificador de rutas'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _mail_post_access = 'read'
    _order = "id desc"
    _check_company_auto = True

    name = fields.Char(string='Nombre', required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    active = fields.Boolean(default=True)
    state_id = fields.Many2one('res.country.state', string='Departamento',
        help="Departamentos")
    user_id = fields.Many2one('res.users', string='Vendedor')
    project_line = fields.One2many('project.task', 'planificador_id', string='Visitas')
    country_id = fields.Many2one('res.country', related = 'company_id.country_id')
    stage = fields.Selection([('pending','Pendiente'),
                                 ('in_process','En proceso'),
                                 ('completed','Completada')], string='Estado', required=True, readonly=True, default='pending')
    def button_in_progress(self):
       self.write({
           'stage': "in_process"
       })
    def button_completed(self):
       self.write({
           'stage': "completed"
       })

    @api.onchange("company_id")
    def _onchange_company_id(self):
        for rec in self:
            return {"domain":{"state_id":[("country_id","=", rec.country_id.id)]}}


class ProjectTask(models.Model):
    _inherit = 'project.task'

    planificador_id = fields.Many2one('planificador.rutas', string='Ruta Planificada',  ondelete='cascade', index=True, copy=False)
    ruta_id = fields.Many2one('rutas', string='Ruta', ondelete='cascade', index=True, copy=False)
    visit_exit = fields.Boolean(string='Visita exitosa', readonly=True, default=False)
    visit_failure_reason = fields.Text(string='Comentarios')
    facturas_pendientes = fields.Many2many('account.move', string='Facturas', readonly=True)
    orden = fields.Integer(string='Orden de visita')
    fuera_ruta = fields.Boolean(string='Fuera de ruta',readonly=True)
    lost_reason = fields.Many2one('crm.lost.reason', 'Razón visita fallida')
    payment_ids = fields.Many2many('account.payment', string='Pagos', readonly=True)
    tarifas = fields.Many2one('product.pricelist', string='Tarifas', related='partner_id.property_product_pricelist')
    invoice_count = fields.Integer(string="Facturas Totales")
    
    @api.model
    def default_get(self, fields):
        res = super(ProjectTask,self).default_get(fields)
        self.invoice_count = self.env['account.move'].search_count([
                ('payment_state', '!=', 'paid'),
                ('state', '=', 'posted'),
                ('partner_id', '=', self.partner_id.id),
                ('move_type', '=', 'out_invoice')])
        return res
      
    def action_open_task_invoices(self):
        invoices = self.env['account.move'].search([
            ('payment_state', '!=', 'paid'),
            ('state', '=', 'posted'),
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', 'out_invoice')
        ])
        action = {
            'name': _('Invoices'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'views': [[False, 'tree'], [False, 'form'], [False, 'kanban']],
            'domain': [('id', 'in', invoices.ids)],
            'context': {
                'create': False,
            }
        }
        return action

    def action_validate(self):
        return {
            'name': _('Estado de visita'),
            'res_model': 'wizard.faild.done',
            'view_mode': 'form',
            'context': {
                'active_model': 'project.task',
                'active_id': self.id,
                },
            'target': 'new',
            'type': 'ir.actions.act_window',
            }

    def ruta_manual(self):
        return {
            'name': _('Ruta Manual'),
            'res_model': 'asistente.asignacion.manual',
            'view_mode': 'form',
            'context': {
                'active_model': 'project.task',
                'active_id': self.id,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
