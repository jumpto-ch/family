from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    statement_name = fields.Char(string="Statement Name",
                                 help="Name to be used in bank statement for retrieving partner")
