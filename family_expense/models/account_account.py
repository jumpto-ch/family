from odoo import api, fields, models, _


class AccountAccount(models.Model):
    _inherit = "account.account"

    description = fields.Char(string="Description", help="Description of the account")


