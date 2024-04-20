# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CahsshInOut(models.TransientModel):
    _name = 'account.bank.statement.in.out'
    _description = 'Create an minimal account bank statement'

    date = fields.Date(require=True, default=fields.Date.context_today)
    amount = fields.Float(string='Amount', required=True)
    description = fields.Char(string='Description')

    def action_post(self):
        journal = self.env['account.journal'].browse(self.env.context.get('default_journal_id'))
        current_balance = journal.default_account_id.current_balance
        moves = self.env['account.bank.statement'].create({
            'journal_id': journal.id,
            'balance_start': current_balance,
            'balance_end_real': current_balance + self.amount,
            'date': self.date,
            'line_ids': [(0, 0, {
                'date': self.date,
                'payment_ref': self.description,
                'amount': self.amount
            })]
        })
        moves.button_post()

        action_id = self.env.ref("account.open_account_journal_dashboard_kanban")
        res = action_id.read()[0]
        res["target"] = "main"
        return res
