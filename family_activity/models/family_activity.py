# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FamilyActivity(models.Model):
    _name = 'family_activity'
    _description = 'Manage an activity for a family'

    name = fields.Char()
    employee_ids = fields.Many2many('hr.employee')

    def action_create_event(self):
        view_id = self.env.ref('family_activity.family_activity_creation_view_wizard_form').id
        context = self._context.copy()
        return {
            'name': 'Create event',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'family.activity.event.wizard',
            'view_id': view_id,
            'target': 'new',
            'context': context,
        }