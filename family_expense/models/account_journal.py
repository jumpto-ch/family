# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    make_quick_payment = fields.Boolean(string="Automatic payment", help="""Make automatic payment on quick expense""")

    def action_month_expense(self):
        self.ensure_one()
        mis_report_id = self.env['mis.report.instance'].search([('budget_view', '=', True)], limit=1)
        view_id = self.env.ref("mis_builder.mis_report_instance_result_view_form")
        return {
            "type": "ir.actions.act_window",
            "res_model": "mis.report.instance",
            "res_id": mis_report_id[0].id,
            "view_mode": "form",
            "view_id": view_id.id,
            "target": "current"
        }

    def action_create_new_entry(self):
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
            'name': _('Create new invoice/bill'),
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
            'name': _('Create new invoice/bill'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move.quick.expense',
            'target': 'new',
            'context': ctx,
        }
