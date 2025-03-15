{
    'name': 'Family Full Expense',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Module to install all family expense modules',
    'description': """
        This module installs all the modules in the family directory.
    """,
    'depends': [
        'contacts',
        'base_automation',
        'family_expense',
        'account_cutoff_start_end_dates',  # https://github.com/OCA/account-closing.git
        'account_financial_report',  # https://github.com/OCA/account-financial-report.git
        'account_reconcile_oca',  # https://github.com/OCA/account-reconcile.git
        'account_statement_import_camt',  # https://github.com/OCA/bank-statement-import.git
        'web_responsive',  # https://github.com/OCA/web.git
    ],
    'data': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
