from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class QuickExpenseWizard(models.TransientModel):
    _name = 'account.move.quick.expense'
    _description = 'Create an account move only with required field'

    partner_id = fields.Many2one('res.partner', string='Vendor')
    description = fields.Char(string='Description')
    account_id = fields.Many2one('account.account', required=True, domain=[('code', '>=', '4000')])
    is_draft = fields.Boolean(string='Draft')
    currency_id = fields.Many2one('res.currency', string='Currency')
    price = fields.Monetary(string='Price', required=True)
    invoice_date = fields.Date(string='Date', default=fields.Date.context_today)
    payment_method = fields.Many2one('account.journal', string='Payment Method', required=True,
                                     domain=[('type', 'in', ('bank', 'cash'))])

#    @api.constrains('account_id')
#    def _check_account_balance(self):
#        for record in self:
#            if record.account_id.current_balance > 0:
#                raise UserError(_('The current balance of the selected account is below zero.'))

    def action_create_expense(self):
        partner_id = self.partner_id if self.partner_id else self.env.ref('family_expense.undefined_res_partner')
        price = float(self.price)
        moves = self.env['account.move'].create({
            'move_type': self.env.context.get('default_move_type'),
            'journal_id': self.env.context.get('default_journal_id'),
            'partner_id': partner_id.id,
            'invoice_date': self.invoice_date,
            'date': self.invoice_date,
            'invoice_line_ids': [(0, 0, {
                'name': self.description,
                'account_id': self.account_id.id,
                'price_unit': price
            })]
        })
        if not self.is_draft:
            moves.action_post()
            moves.message_post(body=f"Paid by {self.payment_method.name}")
            if self.payment_method.make_quick_payment:
                payment = self.env['account.payment.register'].with_context({
                    'active_model': 'account.move',
                    'active_ids': moves.ids,
                    'dont_redirect_to_payments': True
                }).create({
                    'journal_id': self.payment_method.id
                })
                payment.action_create_payments()

            if self.payment_method.make_quick_payment:
                statement_line = self.env['account.bank.statement.line'].create({
                    'journal_id': self.payment_method.id,
                    'amount': -price,
                    'date': self.invoice_date,
                    'manual_name': self.description,
                    'partner_id': partner_id.id,
                })

        action_id = self.env.ref("account.open_account_journal_dashboard_kanban")
        res = action_id.read()[0]
        res["target"] = "main"
        return res
