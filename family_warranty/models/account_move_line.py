# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    has_vendor_warranty = fields.Boolean()
    vendor_warranty_limit = fields.Date()

    @api.onchange('has_vendor_warranty')
    def _onchange_has_vendor_warranty(self):
        self.vendor_warranty_limit =\
            fields.Datetime.now() + relativedelta(years=2) if self.has_vendor_warranty else False

    @api.constrains('move_id', 'has_vendor_warranty', 'vendor_warranty_limit')
    def _check_warranty(self):
        for line in self:
            if (line.has_vendor_warranty is True
                    and line.vendor_warranty_limit is False):
                raise ValidationError(_('The vendor warranty limit cannot be empty if a warranty have been define'))
            move_id = line.move_id
            if (move_id.state != 'draft'
                    and line.has_vendor_warranty is True
                    and move_id.message_attachment_count == 0):
                raise ValidationError(_('There has to have at least one attachment if a vendor warranty have been define'))
        return True
