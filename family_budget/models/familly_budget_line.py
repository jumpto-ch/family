# -*- coding: utf-8 -*-

from odoo import fields, models, _

class FamillyBudgetLine(models.Model):
    _name = "familly.budget.line"
    _description = "Budget Line"

    budget_id = fields.Many2one('familly.budget', string='Budget', required=True)
    account_id = fields.Many2one('account.account', string='Account', required=True)
    company_id = fields.Many2one(
        'res.company', string='company',
        default=lambda self: self.env.company
    )
    amount = fields.Float(required=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string='Label')
    currency_id = fields.Many2one(
        related="company_id.currency_id",
        string="Company Currency",
        readonly=True,
        store=True
    )

    type = fields.Selection([
        ('income', 'Income'),
        ('expense', 'Expense')
    ], required=True)
