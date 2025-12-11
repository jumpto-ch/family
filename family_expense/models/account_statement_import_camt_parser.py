
from odoo import fields, models, api, _


class AccountStatementImportCamtParser(models.AbstractModel):
    _inherit = "account.statement.import.camt.parser"

    def parse_statement(self,  ns, node):
        result = super().parse_statement(ns, node)

        # Use custom statement_name to find partners in narration
        def _find_matching_partner(search_string):
            for p in self.env['res.partner'].search([]):
                criteria = p.statement_name.lower() if p.statement_name else p.name.lower()
                if isinstance(criteria, str) and criteria in search_string.lower():
                    return p
                else:
                    return None

        # Change the partner of specific bank and partner combinations
        # to find one more specific partner based on the narration (ustrd)
        bank_filter = ['BCJUCH22XXX']
        partner_filter = ['Stéphane Eicher']
        bank_node = node.xpath("./ns:Acct/ns:Svcr/ns:FinInstnId/ns:BICFI", namespaces={"ns": ns})
        ustrd_key = "%s (RmtInf/Ustrd)" % _("Unstructured Reference")

        for transaction in result['transactions']:
            if 'partner_name' in transaction.keys() and 'partner_id' not in transaction.keys():
                # find the correct partner
                filtered_partner = None
                partner = _find_matching_partner(transaction['partner_name'])
                if partner:
                    # if partner and bank match filters
                    if (bank_node and bank_node[0].text in bank_filter and
                            partner.name.lower() in [p.lower() for p in partner_filter]):
                        # and if ustrd exists in narration, use it to find more specific partner
                        research_string = transaction['narration'][ustrd_key].lower()\
                            if ustrd_key in transaction['narration'].keys() else ''
                        filtered_partner = _find_matching_partner(research_string)

                    if filtered_partner:
                        transaction['partner_id'] = filtered_partner.id
                    else:
                        transaction['partner_id'] = partner.id

        return result
