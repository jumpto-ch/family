{
    'name': 'Family Full Expense',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Module to install all family expense modules',
    'description': """
        This module installs all the modules in the family directory.
    """,
    'depends': [
        'family_expense',
        'account_statement_import_camt',  # https://github.com/OCA/bank-statement-import.git
        'account_reconcile_oca',  # https://github.com/OCA/account-reconcile.git
    ],
    'data': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
