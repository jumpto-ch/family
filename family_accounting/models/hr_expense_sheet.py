# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Expense(models.Model):
    _inherit = 'hr.expense.sheet'

    # Remove activity to approve expense
    def activity_update(self):
        pass
