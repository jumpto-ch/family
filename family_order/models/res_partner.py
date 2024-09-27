# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"
    _order = "invoices_count DESC"

    invoices_count = fields.Integer(
        compute='_compute_invoices_count',
        store=True,
    )

    @api.depends('invoice_ids')
    def _compute_invoices_count(self):
        for p in self:
            p.invoices_count = len(p.invoice_ids)

    def _get_name_search_order_by_fields(self):
        return f"invoices_count DESC, {super()._get_name_search_order_by_fields()}"
