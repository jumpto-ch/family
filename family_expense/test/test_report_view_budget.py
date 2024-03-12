# Copyright 2024 JumpTo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import doctest

from odoo.tests import BaseCase, tagged

from odoo.tests.common import TransactionCase


class TestBudgetView(TransactionCase):

    def setUp(self):
        super().setUp()

    def test_view_budget(self):
        # test view budget

        pass