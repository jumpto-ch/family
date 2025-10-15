from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import ast


class QuickExpenseWizard(models.TransientModel):
    _name = 'account.journal.cash.in.out'
    _description = 'Make an automatic cash in or out entry'

    description = fields.Char(string='Description', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    amount = fields.Monetary(string='Amount', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)

    account_id = fields.Many2one('account.account', string='Account', domain=lambda self: self._get_cash_journal_domain())
    partner_id = fields.Many2one('res.partner', string='Partner')
    
    @api.model
    def _get_cash_journal(self):
        journal = self.env['account.journal'].search([
            ('type', '=', 'cash'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        return journal

    def _get_cash_journal_domain(self):
        journal = self._get_cash_journal()
        if journal and journal.quick_transaction_account_domain:
            import ast
            try:
                return ast.literal_eval(journal.quick_transaction_account_domain)
            except Exception:
                return []
        return []

    @api.constrains('amount')
    def _check_amount_positive(self):
        for rec in self:
            if rec.amount < 0:
                raise ValidationError(_('The amount must be positive.'))


    def action_cash(self):
        
        amount = float(self.amount)
        if self.env.context.get('direction') == 'out':
            amount = -amount
            
        cash_journal = self._get_cash_journal()
        
        statement = self.env['account.bank.statement'].search([
            ('journal_id', '=', cash_journal.id),
            ('date', '=', self.date),
        ], limit=1)

        if not statement:
            statement = self.env['account.bank.statement'].create({
                'journal_id': cash_journal.id,
                'date': self.date,
            })

        
        statement_line_vals = {
            'statement_id': statement.id,
            'date': self.date,
            'amount': amount,
            'payment_ref': self.description,
        }
        if self.partner_id:
            statement_line_vals['partner_id'] = self.partner_id.id

        self.env['account.bank.statement.line'].create(statement_line_vals)

        
        if self.account_id:
            # Create the corresponding accounting entry
            move = self.env['account.move'].create({
                'move_type': 'entry',
                'journal_id': cash_journal.id,
                'date': self.date,
                'line_ids': [
                    (0, 0, {
                        'account_id': cash_journal.default_account_id.id,
                        'debit': self.amount if self.env.context.get('direction') == 'in' else 0.0,
                        'credit': 0.0 if self.env.context.get('direction') == 'in' else self.amount,
                        'name': self.description or '',
                        'partner_id': self.partner_id.id if self.partner_id else False,
                    }),
                    (0, 0, {
                        'account_id': self.account_id.id,
                        'debit': 0.0 if self.env.context.get('direction') == 'in' else self.amount,
                        'credit': self.amount if self.env.context.get('direction') == 'in' else 0.0,
                        'name': self.description or '',
                        'partner_id': self.partner_id.id if self.partner_id else False,
                    }),
                ],
            })
            move.action_post()
            statement.line_ids.filtered(lambda l: l.payment_ref == self.description).write({
                'move_id': move.id
            })
        
        return {'type': 'ir.actions.act_window_close'}
       
