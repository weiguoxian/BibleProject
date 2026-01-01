#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =====================================================
#  Copyright (c) 2025 GREGORY
#  Description : test_ecdict.py
#  Author      : weiguoxian@gmail.com
#  Created     : 2026-01-01
#  License     : MIT License
# =====================================================
import os
import unittest

from src.lib import ecdict


PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class TestEcdict(unittest.TestCase):
    def test_load_ecdict(self):
        word_ecdict = ecdict.load_ecdict(os.path.join(PROJ_ROOT, "src/data", "ecdict.csv"))
        self.assertGreaterEqual(len(word_ecdict), 160884)  # add assertion here


if __name__ == '__main__':
    unittest.main()
