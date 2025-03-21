# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import re

from odoo import models
from odoo.osv.expression import get_unaccent_wrapper
from odoo.tools import html2plaintext

from odoo.addons.base.models.res_bank import sanitize_account_number


class AccountBankStatementLine(models.Model):
    _inherit = ("account.bank.statement.line",)

    def create(self, vals):
        new_vals = []
        for val in vals:
            if 'partner_id' not in val.keys() and 'partner_name' not in val.keys():
                for company in self.env['res.partner'].search([('is_company', '=', 'true')]):
                    if company.name and company.name.lower() in val['narration'].lower():
                        val['partner_id'] = company.id
                        break

            if 'payment_ref' not in val.keys() or val['payment_ref'] == '/':

                if 'Additional Entry Information (AddtlNtryInf):' in val['narration']:
                    match = re.search(r'Additional Entry Information \(AddtlNtryInf\):([^\n]*)', val['narration'])
                    if match:
                        val['payment_ref'] = match.group(1).strip()

            new_vals.append(val)

        res = super().create(new_vals)
        return res
