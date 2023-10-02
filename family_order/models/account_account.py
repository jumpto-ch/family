# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountAccount(models.Model):
    _inherit = "account.account"
    _order = "moves_count DESC"

    moves_count = fields.Integer(
        compute='_compute_moves_count',
        store=True,
    )
    move_ids = fields.One2many('account.move.line', 'account_id')

    @api.depends('move_ids')
    def _compute_moves_count(self):
        for a in self:
            a.moves_count = len(a.move_ids)

    def _get_name_search_order_by_fields(self):
        return f"moves_count DESC, {super()._get_name_search_order_by_fields()}"
