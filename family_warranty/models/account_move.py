# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.constrains('state', 'line_ids', 'message_attachment_count')
    def _check_warranty(self):
        for move_id in self:
            if (move_id.state != 'draft'
                    and True in move_id.line_ids.mapped('has_vendor_warranty')
                    and move_id.message_attachment_count == 0):
                raise ValidationError(_('There has to have at least one attachment if a vendor warranty have been define'))