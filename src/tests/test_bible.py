#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =====================================================
#  Copyright (c) 2025 GREGORY
#  Description : test_bible.py
#  Author      : weiguoxian@gmail.com
#  Created     : 2025-12-13
#  License     : MIT License
# =====================================================
import unittest

from src.lib.bible import Words


class TestWords(unittest.TestCase):
    def test_get_word_cn_def(self):
        words = Words()
        ans = words.get_word_definitions(word="cognitive")
        self.assertEqual(len(ans), 1)


if __name__ == '__main__':
    unittest.main()
