
from odoo import fields, models, api, _
import re

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
            return None

        # Change the partner_id of specific bank and partner combinations
        # to find one more specific partner based on the narration
        bank_filter = ['BCJUCH22XXX']
        # Each entry is a list of name parts where ALL MUST be present in the partner name
        # each name part can have multiple possible solutions, only ONE needs to match
        # ex: Eicher Stéphane / Stephane Eicher will match
        # ( list_of_partners/any: (list_of_conditions/all: (list_of_possible_solutions_in_name/any: Stephan, Steph ) )
        partner_list_filter = [
            (
                ('Stéphane', 'Stephane', 'Steph'),
                ('Eicher')
            ),
            (
                ('Alyssia'),
                ('Eicher', 'Broquet')
            )]
        bank_node = node.xpath("./ns:Acct/ns:Svcr/ns:FinInstnId/ns:BICFI", namespaces={"ns": ns})
        # Pattern could be RmtInf/Ustrd - AddtlTxInf - AddtlNtryInf - Refs/InstrId
        new_fields_pattern = ["RmtInf/Ustrd"]

        for transaction in result['transactions']:
            if 'partner_name' in transaction.keys() and 'partner_id' not in transaction.keys():
                # find the correct partner
                filtered_partner = None
                partner = _find_matching_partner(transaction['partner_name'])
                if partner:
                    # if partner and bank match filters
                    partner_name = partner.statement_name if partner.statement_name else partner.name
                    if (bank_node and bank_node[0].text in bank_filter and
                        any(all(any(solution in partner_name for solution in condition)
                                for condition in partner_filter)
                            for partner_filter in partner_list_filter)):
                        # try to find specific field in narration
                        for new_field_pattern in new_fields_pattern:
                            match = re.search(rf'\({new_field_pattern}\):([^\n]*)',
                                              transaction['narration'])

                            # if field exist in narration, try to find matching partner
                            research_string = match.group(1).strip() if match else ''
                            filtered_partner = _find_matching_partner(research_string)
                            # if more specific partner found, stop searching
                            if filtered_partner:
                                transaction['partner_id'] = filtered_partner.id
                                break
                        # partner in filter but no more specific partner found, remove partner
                        if not filtered_partner:
                            transaction['partner_id'] = False
                    else:
                        # partner is found but not in filter, use it
                        transaction['partner_id'] = partner.id

        return result
