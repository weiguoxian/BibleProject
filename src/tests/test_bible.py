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

from src.lib.bible import Word


class TestWord(unittest.TestCase):
    def test_get_word_cn_def(self):
        words = Word()
        ans = words.get_word_definitions(word="cognitive")
        self.assertEqual(len(ans), 1)

    def test_get_bible_words(self):
        word = Word()
        words = word.get_bible_words()
        self.assertGreaterEqual(len(words), 10000)

    def test_gen_bible_words(self):
        word = Word()
        word_dict = {
            "cognitive": {
                "freq": 23456,
                "example": "xxxx"
            },
            "in": {
                "freq": 21456,
                "example": "yyyy"
            }
        }
        ans = word.gen_bible_words(word_dict)
        self.assertGreaterEqual(ans, 0)


if __name__ == '__main__':
    unittest.main()
