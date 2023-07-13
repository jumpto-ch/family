# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def write(self, vals):
        result = super().write(vals)
        for payment in self:
            statement = self.env['account.bank.statement'].search([('name', '=', payment.name)])
            if payment.state == 'posted':
                if not statement:
                    new_statement = self.env['account.bank.statement'].create({
                        'name': payment.name,
                        'journal_id': payment.journal_id.id,
                        'date': payment.date,
                        'line_ids': [(0, 0, {
                            'date': payment.date,
                            'amount': -payment.amount,
                            'payment_ref': payment.ref,
                            'partner_id': payment.partner_id.id
                        })]
                    })
                    new_statement.button_post()
        return result
