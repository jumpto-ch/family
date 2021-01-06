# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    is_family = fields.Boolean(string='Is a Family', default=False,
                               help="Check if the contact is a family")
    company_type = fields.Selection(selection_add=[('family', 'Family')])

    @api.depends('child_ids', 'is_family')
    def _compute_display_name(self):
        super(Partner, self)._compute_display_name()

    @api.depends('is_family')
    def _compute_company_type(self):
        super(Partner, self)._compute_company_type()
        for partner in self:
            if partner.is_family:
                partner.company_type = 'family'

    def _write_company_type(self):
        super(Partner, self)._write_company_type()
        for partner in self:
            partner.is_company = partner.is_family = partner.company_type == 'family'

    def onchange_company_type(self):
        if self.company_type == 'company':
            self.is_company = True
            self.is_family = False
        elif self.company_type == 'family':
            self.is_company = self.is_family = True
        else:
            self.is_company = self.is_family = False

    def _get_family_name(self, partner, name):
        return 'Family ' + name + ', ' + ', '.join(partner.child_ids.mapped('name'))

    def _get_name(self):
        name = super(Partner, self)._get_name()
        if self.is_family:
            name = self._get_family_name(self, name)
        return name
