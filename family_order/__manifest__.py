# -*- coding: utf-8 -*-
{
    'name': "family_order",

    'summary': """
        Order in acccount and partner by move
        """,

    'description': """
        This module change default order in view of accounts and partner to be the the one with the most move
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
    ],
}
