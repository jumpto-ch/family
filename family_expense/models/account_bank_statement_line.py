import logging
import re

from odoo import models

_logger = logging.getLogger(__name__)

class AccountBankStatementLine(models.Model):
    _inherit = ("account.bank.statement.line",)

    def create(self, vals):
        # si vals n'est pas une liste transformer en liste
        vals = [vals] if not isinstance(vals, list) else vals
        new_vals = []
        for val in vals:
            if 'payment_ref' not in val.keys() or val['payment_ref'] == '/':

                if 'Additional Entry Information (AddtlNtryInf):' in val['narration']:
                    match = re.search(r'Additional Entry Information \(AddtlNtryInf\):([^\n]*)', val['narration'])
                    if match:
                        val['payment_ref'] = match.group(1).strip()

            if 'partner_name' in val.keys() and 'partner_id' not in val.keys():
                for partner in self.env['res.partner'].search([]):
                    # log statement_name in debug
                    _logger.warning("partner_name: %s", partner.id)
                    statement_name = partner.statement_name.lower() if partner.statement_name else partner.name.lower()
                    state_line_ref = val['partner_name'].lower()

                    if isinstance(statement_name, str) and statement_name in state_line_ref:
                        val['partner_id'] = partner.id
                        break

            if 'partner_id' not in val.keys() and 'partner_name' not in val.keys():
                for partner in self.env['res.partner'].search([]):
                    state_line_ref = val['payment_ref'].lower()
                    statement_name = partner.statement_name.lower() if partner.statement_name else partner.name.lower()

                    if isinstance(statement_name, str) and statement_name in state_line_ref:
                        val['partner_id'] = partner.id
                        break

                    #log statement_name in debug
                    _logger.warning("partner_name: %s", partner.name)
                    _logger.warning("statement_name: %s", statement_name)
                    _logger.warning("test: %s", isinstance(statement_name, str) and statement_name in state_line_ref)



            new_vals.append(val)

        res = super().create(new_vals)
        return res
