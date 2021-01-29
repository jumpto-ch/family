# -*- coding: utf-8 -*-
{
    'name': "family_base",

    'summary': """
        This module aim to help to manage a family""",

    'description': """
        This module aim to help to manage a family
    """,

    'author': "JumpTo",
    'website': "http://jumpto.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sms', 'contacts'],

    # always loaded
    'data': ['views/res_partner_views.xml'],
}
