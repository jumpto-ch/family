# -*- coding: utf-8 -*-
{
    'name': "family_activity",

    'summary': """
        This module aim to help family to manage their activities""",

    'description': """
        This module aim to help family to manage their activities
    """,

    'author': "JumpTo",
    'website': "http://jumpto.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/family_activity_view.xml',
        'wizard/family_activity_create_event_wizard_view.xml'
    ],
}
