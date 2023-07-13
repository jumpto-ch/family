# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    make_automatic_bank_statement = fields.Boolean(
        string="Automatic bank statement",
        help="""Create a new statement when a new payment is done on this journal""")
