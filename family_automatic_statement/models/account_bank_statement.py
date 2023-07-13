# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    @api.depends('previous_statement_id', 'previous_statement_id.balance_end_real')
    def _compute_ending_balance(self):
        super()._compute_ending_balance()
        for statement in self:
            if statement.journal_id.make_automatic_bank_statement:
                total_entry_encoding = sum([line.amount for line in statement.line_ids])
                statement.balance_end_real = statement.previous_statement_id.balance_end_real + total_entry_encoding