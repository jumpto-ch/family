# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FamilyActivityEvent(models.TransientModel):
    _name = 'family.activity.event.wizard'
    _description = 'Wizard to create event from family activity'

    datetime = fields.Datetime()

    def create_event(self):
        context = self._context.copy()
        return context
