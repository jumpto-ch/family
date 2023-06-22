# -*- coding: utf-8 -*-
{
    'name': "family_warranty",

    'summary': """
            Add the possibility to set a vendor warranty to a invoice line, require a pdf before you can post the invoice
        """,

    'description': """
        Add the possibility to set a vendor warranty to a invoice line, require a pdf before you can post the invoice
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
        'views/vendor_warranty.xml',
        'views/warranty_menu.xml'
    ],
}
