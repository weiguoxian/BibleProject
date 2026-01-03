#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =====================================================
#  Copyright (c) 2025 GREGORY
#  Description : test_bible.py
#  Author      : weiguoxian@gmail.com
#  Created     : 2025-12-13
#  License     : MIT License
# =====================================================
import os
import time
import unittest
import pandas

from src.lib.bible import Word

PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

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
        """单元测试：生成圣经单词"""
        word = Word()
        word_dict = {
            "cognitive": {
                "freq": 23456,
                "hold": "NO",
                "pos": "x",
                "definition_en": "xxxx",
                "definition_zh": "xxxx",
                "bible_examples": "xxxx"
            },
            "in": {
                "freq": 21456,
                "hold": "YES",
                "pos": "y",
                "definition_en": "yyyy",
                "definition_zh": "yyyy",
                "bible_examples": "yyyy"
            }
        }
        ans = word.gen_bible_words(word_dict)
        self.assertGreaterEqual(len(ans), 2)

    def test_report_bible_words(self):
        """单元测试：生成excel报表"""
        word = Word()
        ans = word.report_bible_words()
        self.assertGreaterEqual(ans, 0)


    def test_parse_bible_words(self):
        """单元测试：解析圣经全量单词表"""
        word = Word()
        ans = word.parse_bible_words(os.path.join(PROJ_ROOT, "src/data", "NIV_Bible_Full_Text.txt"))
        self.assertGreaterEqual(len(ans), 5000)


if __name__ == '__main__':
    unittest.main()
