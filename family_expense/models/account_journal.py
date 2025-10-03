# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    make_quick_payment = fields.Boolean(string="Automatic payment", help="""Make automatic payment on quick expense""")
    make_quick_transaction = fields.Boolean(string="Automatic transaction", help="""Show the Cash in/out button on the dashboard""")

    def action_create_new_entry(self):
        """Special action on the dashboard view"""
        ctx = self._context.copy()
        ctx['default_journal_id'] = self.id
        if self.type == 'sale':
            ctx['default_move_type'] = 'out_refund' if ctx.get('refund') else 'out_invoice'
        elif self.type == 'purchase':
            ctx['default_move_type'] = 'in_refund' if ctx.get('refund') else 'in_invoice'
        return {
            'name': _('New Expense'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move.quick.expense',
            'target': 'new',
            'context': ctx,
        }

    def action_cash_in_out(self):
        """Special action on the dashboard view"""
        ctx = self._context.copy()
        ctx['default_journal_id'] = self.id
        if self.type == 'sale':
            ctx['default_move_type'] = 'out_refund' if ctx.get('refund') else 'out_invoice'
        elif self.type == 'purchase':
            ctx['default_move_type'] = 'in_refund' if ctx.get('refund') else 'in_invoice'
        else:
            ctx['default_move_type'] = 'entry'
            ctx['view_no_maturity'] = True
        return {
            'name': _('New cash in/out'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move.quick.expense',
            'target': 'new',
            'context': ctx,
        }
        
    def _get_journal_dashboard_data_batched(self):
        """ Override to add quick expense parameter """
        res = super()._get_journal_dashboard_data_batched()
        for journal in self:
            res[journal.id]['make_quick_transaction'] = journal.make_quick_transaction
        return res
