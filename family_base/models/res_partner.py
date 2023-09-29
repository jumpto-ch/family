# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    is_family = fields.Boolean(string='Is a Family', default=False,
                               help="Check if the contact is a family")
    is_family_member = fields.Boolean(string='Is a member of a family', compute='_compute_is_family_member', store=True,
                                      help="Check if the contact is a member of a family")
    company_type = fields.Selection(selection_add=[('family', 'Family')])
    family_member_role = fields.Selection([('parent', 'Parent'), ('child', 'child')], 'Role')

    @api.depends('is_family', 'child_ids', 'child_ids.family_member_role')
    def _compute_display_name(self):
        super(Partner, self)._compute_display_name()

    @api.depends('is_company', 'is_family')
    def _compute_company_type(self):
        for partner in self:
            if partner.is_family:
                partner.company_type = 'family'
            elif partner.is_company:
                partner.company_type = 'company'
            else:
                partner.company_type = 'person'

    def _write_company_type(self):
        for partner in self:
            partner.write({
                'is_company': partner.company_type in ['company', 'family'],
                'is_family': partner.company_type == 'family'})

    @api.onchange('company_type')
    def onchange_company_type(self):
        if self.company_type == 'company':
            self.is_company = True
            self.is_family = False
        elif self.company_type == 'family':
            self.is_company = self.is_family = True
        else:
            # noinspection PyAttributeOutsideInit
            self.is_company = self.is_family = False

    @api.depends('is_company', 'parent_id', 'parent_id.is_family')
    def _compute_is_family_member(self):
        for partner in self:
            partner.is_family_member = partner.parent_id.is_family and not partner.is_company

    def _get_family_name(self, partner, name):
        parent = partner.child_ids.filtered(lambda c: c.family_member_role == 'parent')
        return 'Family ' + name + ', ' + ' & '.join(parent.mapped('name'))

    def _get_name(self):
        name = super(Partner, self)._get_name()
        if self.is_family:
            name = self._get_family_name(self, name)
        return name
