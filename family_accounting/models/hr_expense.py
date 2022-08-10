# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Expense(models.Model):
    _inherit = 'hr.expense'

    payment_mode = fields.Selection(default='company_account')
    name = fields.Char("Name")
    remarks = fields.Char("Description")
    vendor_id = fields.Many2one('res.partner')

    @api.onchange('remarks', 'product_id')
    def _onchange_remarks(self):
        if self.remarks:
            self.name = self.product_id.display_name + ' - ' + self.remarks

    # Set vendor as partner for account.move.line
    def _get_account_move_line_values(self):
        return_dict = super(Expense, self)._get_account_move_line_values()
        for key in return_dict:
            expense = self.browse(key)
            result_vals = []
            for vals in return_dict[key]:
                vals['partner_id'] = expense.vendor_id.id
                result_vals.append(vals)
            return_dict[key] = result_vals
        return return_dict

    # Auto submit report
    def action_submit_expenses(self):
        return_dict = super(Expense, self).action_submit_expenses()
        sheet = self.env['hr.expense.sheet'].browse(return_dict['res_id'])
        sheet.action_submit_sheet()
        sheet.approve_expense_sheets()
        sheet.action_sheet_move_create()
        return return_dict
