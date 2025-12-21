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
        self.assertGreaterEqual(ans, 0)

    def test_gen_excel_output(self):
        # 1. 定义表头
        columns = ["word", "freq", "pos", "meaning"]

        # 2. 行容器逐行追加数据
        rows = [["love", 120, "noun", "爱"], ["faith", 95, "noun", "信心"], ["believe", 80, "verb", "相信"]]

        # 4. 生成 DataFrame
        df = pandas.DataFrame(rows, columns=columns)

        # 5. 写入 Excel
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        output = os.path.join(PROJ_ROOT, "output", f"bible_words_full_{time_str}.xlsx")
        df.to_excel(output, sheet_name="Sheet1", index=False)

        print("Excel 写入完成")

if __name__ == '__main__':
    unittest.main()
