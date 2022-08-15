# -*- coding: utf-8 -*-
{
    'name': "family_accounting",

    'summary': """
        This module aim to help to manage a family accounting""",

    'description': """
        This module aim to help to manage a accounting for a family
    """,

    'author': "JumpTo",
    'website': "http://jumpto.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '13.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['hr_expense_journal','family_base'],

    # always loaded
    'data': ['views/hr_expense.xml',
             'views/hr_expense_sheet.xml'
             ],
}
