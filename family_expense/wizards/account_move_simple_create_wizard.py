# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountMoveSimpleCreateWizard(models.TransientModel):
    _name = 'account.move.simple.create.wizard'
    _description = 'Create an account move only with required field'

    partner_id = fields.Many2one('res.partner', string='Partner')
    account_id = fields.Many2one('account.account')
    account_payment_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Journal',
        domain="[('type', 'in', ('bank','cash'))]")

    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
    invoice_date = fields.Date(string='Invoice/Bill Date', default=fields.Date.context_today)

    def action_post(self):
        moves = self.env['account.move'].create({
            'move_type': self.env.context.get('default_move_type'),
            'journal_id': self.env.context.get('default_journal_id'),
            'partner_id': self.partner_id,
            'invoice_date': self.invoice_date,
            'date': self.invoice_date,
            'invoice_line_ids': [(0, 0, {
                'account_id': self.account_id,
                'price_unit': self.price_unit
            })]
        })
        moves.action_post()
        wizards = self.env['account.payment.register'].with_context({
                'active_model': 'account.move',
                'active_ids': moves.ids,
                'dont_redirect_to_payments': True
            }).create({
                'journal_id': self.account_payment_journal_id.id
            })
        wizards.action_create_payments()
