from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MisReportInstance(models.Model):
    _inherit = "mis.report.instance"

    budget_view = fields.Boolean(string="Budget view", help="Button budget on the card", copy=False)

    @api.constrains('budget_view')
    def _check_budget_view(self):
        if self.env['mis.report.instance'].search_count([('budget_view', '=', True)]) > 1:
            # show user odoo error message
            raise ValidationError(_("You can only have one budget view"))
