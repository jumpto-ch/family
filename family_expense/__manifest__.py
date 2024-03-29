# -*- coding: utf-8 -*-
{
    'name': "family_expense",

    'summary': """
        This module add a button to the accounting dashboard view to speed and simplify the entry of expense
        """,

    'description': """
        This module add a button to the accounting dashboard view to speed and simplify the entry of expense
        """,

    "license": "AGPL-3",
    'author': "JumpTo",
    'website': "http://jumpto.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '15.0.1.0.0',
    'depends': ['account', 'mis_builder'],

    # always loaded
    'data': [
        'data/res_partner.xml',
        'security/ir.model.access.csv',
        'views/account_journal_views.xml',
        'views/account_account_views.xml',
        'views/mis_report_instance.xml',
        'wizards/account_move_quick_expense_wizard_views.xml'
    ],
}
