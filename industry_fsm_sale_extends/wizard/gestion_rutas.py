# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

logger = logging.getLogger( __name__)

class GestionRutas(models.TransientModel):
    _name = "wizard.gestion.rutas"
    _description = "Asistente para la gestion de rutas"
    name = fields.Char(string="Nombre")
    user_id = fields.Many2one('res.users', string="Vendedor")
    rutas_ids = fields.Many2many('rutas', string="Rutas")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)
    date_start = fields.Date(string="Fecha Inicio", default=fields.Date.today(), required=True)
    date_end = fields.Date(string="Fecha Fin", default=fields.Date.today(), required=True)

    def action_rutas(self):
        self.ensure_one()
        rutas_ids = self.rutas_ids.ids
        proyecto = self.env['project.project'].search([('name', '=', 'Servicio externo')])
        if not rutas_ids:
            raise UserError(_("Debe seleccionar al menos una ruta"))
        planificador = self.env['planificador.rutas']
        for ruta in self.rutas_ids:
            user_id = self.user_id.id
            if not user_id:
                if not ruta.user_id:
                    raise UserError(_("Debe seleccionar un vendedor"))
                user_id = ruta.user_id.id
            partner_ids = ruta.partner_ids
            if partner_ids:
                planificador_id = planificador.create({'name': '{} - {}'.format(ruta.name,self.date_start), 'user_id': user_id, 'state_id': ruta.state_id.id})
                for partner_id in partner_ids:
                    account_move = self.env['account.move'].search([('partner_id', '=', partner_id.partner_id.id), ('state', '=', 'posted'),('payment_state','in',['not_paid','partial'])])
                    project_task = self.env['project.task'].create({
                        'name': '{} - {} '.format(partner_id.partner_id.name, self.date_start),
                        'user_ids': [(4, user_id)],
                        'date_deadline': self.date_end,
                        'date_assign': self.date_start,
                        'date_end': self.date_end,
                        'planned_date_begin': self.date_start,
                        'planned_date_end': self.date_end,
                        'partner_id': partner_id.partner_id.id,
                        'planificador_id': planificador_id.id,
                        'ruta_id': ruta.id,
                        'company_id': self.company_id.id,
                        'active': True,
                        'project_id': proyecto.id,
                        
                        'orden': partner_id.orden,

                    })
                activity = self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'user_id': user_id,
                    'date_deadline': self.date_start,
                    'res_id': planificador_id.id,
                    'automated': True,
                    'res_name':'Ruta planificada',
                    'summary': planificador_id.name,
                    'note': 'Ruta planificada',
                    'res_model_id': self.env['ir.model']._get('planificador.rutas').id,
                })

class AsistenteAsignacionManual(models.Model):
    _name = "asistente.asignacion.manual"
    _description = "Asistente para la asignacion manual de rutas"

    name = fields.Char(string="Nombre", default="Asignacion manual")
    partner_ids = fields.Many2many('res.partner', string="Clientes", required=True)

    def action_asignacion_manual(self):
        self.ensure_one()
        context = self.env.context
        print(context)
        project_task_id = self.env['project.task'].search([('id', '=', context.get('active_id'))])
        if project_task_id:
            planificador_id = project_task_id.planificador_id
            if planificador_id:
                for partner_id in self.partner_ids:
                    partner = self.env['project.task'].search([('partner_id', '=', partner_id.id),('planificador_id', '=', planificador_id.id)])
                    if partner:
                        continue
                    proyecto = self.env['project.project'].search([('name', '=', 'Servicio externo')])
                    account_move = self.env['account.move'].search([('partner_id', '=', partner_id.id), ('state', '=', 'posted'),('payment_state','in',['not_paid','partial'])])
                    project_task = self.env['project.task'].create({
                        'name': '{} - {} '.format(partner_id.name, project_task_id.date_assign),
                        'user_ids': [(4, project_task_id.user_ids.ids[0])],
                        'date_deadline': project_task_id.date_deadline,
                        'date_assign': project_task_id.date_assign,
                        'date_end': project_task_id.date_end,
                        'planned_date_begin': project_task_id.planned_date_begin,
                        'planned_date_end': project_task_id.planned_date_end,
                        'partner_id': partner_id.id,
                        'planificador_id': planificador_id.id,
                        'ruta_id': project_task_id.ruta_id.id,
                        'company_id': project_task_id.company_id.id,
                        'active': True,
                        'project_id': proyecto.id,
                        'facturas_pendientes': [(6, 0, account_move.ids)],
                        'orden': 1,
                        'fuera_ruta': True,
                    })

class WizarFaildDone(models.TransientModel):
    _name = 'wizard.faild.done'
    _description = 'Ventana emergente que permite seleccionar si la visita fue fallida o exitosa'

    state_visit = fields.Selection([('faild','Visita fallida'),
                                     ('done','Visita exitosa')], 
                                    string = "Estado de Visita", default='done')
    text = fields.Text(string='Comentarios') 
    lost_reason_id = fields.Many2one('crm.lost.reason', string = 'Razón de visita fallida')

    def validate_visit(self):
        
        active_ids = self.env.context.get('active_ids')
        move_obj = self.env['project.task']
        for task in move_obj.browse(active_ids):
            if self.state_visit=='done':
                task.visit_exit = True
                task.kanban_state = 'done'
                task.action_fsm_validate()
            else:
                task.visit_exit = False
                task.kanban_state = 'blocked'
                task.lost_reason = self.lost_reason_id
                task.visit_failure_reason = self.text
                task.action_fsm_validate()