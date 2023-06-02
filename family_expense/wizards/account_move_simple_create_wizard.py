# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class QuickExpenseWizard(models.TransientModel):
    _name = 'account.move.quick.expense'
    _description = 'Create an account move only with required field'

    partner_id = fields.Many2one('res.partner', string='Vendor')
    description = fields.Char(string='Description')
    account_id = fields.Many2one('account.account',
                                 required=True,
                                 domain="['|', '|', "
                                        "('code', '=like', '4%'), "
                                        "('code', '=like', '5%'), "
                                        "('code', '=like', '6%'),]")
    payment_method = fields.Many2one(
        comodel_name='account.journal',
        string='Payment method',
        domain="[('type', 'in', ('bank','cash'))]")

    price = fields.Char(string='Price', required=True)
    invoice_date = fields.Date(string='Date', default=fields.Date.context_today)

    @api.constrains('price')
    def _check_price(self):
        for expense in self:
            try:
                val = float(expense.price)
                return True
            except ValueError:
                raise ValidationError(_('The price is not correct'))

    def action_post(self):
        partner_id = self.partner_id if self.partner_id else self.env.ref('family_expense.undefined_res_partner')
        price = float(self.price)
        moves = self.env['account.move'].create({
            'move_type': self.env.context.get('default_move_type'),
            'journal_id': self.env.context.get('default_journal_id'),
            'partner_id': partner_id,
            'invoice_date': self.invoice_date,
            'date': self.invoice_date,
            'invoice_line_ids': [(0, 0, {
                'name': self.description,
                'account_id': self.account_id,
                'price_unit': price
            })]
        })
        moves.action_post()

        if self.payment_method.type == 'cash':
            payment = self.env['account.payment.register'].with_context({
                'active_model': 'account.move',
                'active_ids': moves.ids,
                'dont_redirect_to_payments': True
            }).create({
                'journal_id': self.payment_method.id
            })
            payment.action_create_payments()
