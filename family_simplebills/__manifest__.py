# -*- coding: utf-8 -*-
{
    'name': "family_simplebills",

    'summary': """
        This module add a button to the accounting dashboard view to speed and simplify the entry of simple bills
        """,

    'description': """
        This module add a button to the accounting dashboard view to speed and simplify the entry of simple bills
        """,

    'author': "JumpTo",
    'website': "http://jumpto.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '15.0.1.0.0',

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_journal_dashboard_simplebills_views.xml',
        'wizards/account_move_simple_create_wizard_views.xml'
    ],
}
