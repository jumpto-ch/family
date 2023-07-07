# -*- coding: utf-8 -*-
{
    'name': "family_automatic_statement",

    'summary': """
        Make new bank statement on new payment
        """,

    'description': """
        Create a new bank statement when you create a new payment 
        if that payment use a journal with the make_automatic_bank_statement option activated
        """,

    "license": "AGPL-3",
    'author': "JumpTo",
    'website': "http://jumpto.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '15.0.1.0.0',
    'depends': ['account'],

    # always loaded
    'data': [
        "views/account_journal_views.xml"
    ],
}
