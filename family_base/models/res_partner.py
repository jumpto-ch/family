# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    is_family = fields.Boolean(string='Is a Family', default=False,
                               help="Check if the contact is a family")
    is_family_member = fields.Boolean(string='Is a member of a family', default=False,
                                      help="Check if the contact is a member of a family")
    company_type = fields.Selection(selection_add=[('family', 'Family')])
    family_member_role = fields.Selection([('parent', 'Parent'), ('child', 'child')], 'Role')

    @api.depends('child_ids', 'is_family', 'child_ids.family_member_role')
    def _compute_display_name(self):
        super(Partner, self)._compute_display_name()

    @api.depends('is_family')
    def _compute_company_type(self):
        super(Partner, self)._compute_company_type()
        for partner in self:
            if partner.is_family:
                partner.company_type = 'family'

    def _write_company_type(self):
        for partner in self:
            if partner.company_type == 'company':
                partner.write({'is_company': True, 'is_family': False})
            elif partner.company_type == 'family':
                partner.write({'is_company': True, 'is_family': True})
            else:
                partner.write({'is_company': False, 'is_family': False})

    @api.onchange('company_type', 'parent_id')
    def onchange_company_type(self):
        if self.company_type == 'company':
            self.is_company = True
            self.is_family = False
            self.is_family_member = False
        elif self.company_type == 'family':
            self.is_company = self.is_family = True
            self.is_family_member = False
        else:
            # noinspection PyAttributeOutsideInit
            self.is_company = self.is_family = False
            if self.parent_id.is_family:
                self.is_family_member = True

    def _get_family_name(self, partner, name):
        parent = partner.child_ids.filtered(lambda c: c.family_member_role == 'parent')
        return 'Family ' + name + ', ' + ' & '.join(parent.mapped('name'))

    def _get_name(self):
        name = super(Partner, self)._get_name()
        if self.is_family:
            name = self._get_family_name(self, name)
        return name
