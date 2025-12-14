#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =====================================================
#  Copyright (c) 2025 GREGORY
#  Description : bible.py
#  Author      : weiguoxian@gmail.com
#  Created     : 2025-12-13
#  License     : MIT License
# =====================================================
import os
import time

import pandas
from nltk.corpus import wordnet as wn
from deep_translator import GoogleTranslator

# 如果第一次使用，取消注释下载 WordNet
# import nltk
# nltk.download('wordnet')
# nltk.download('omw-1.4')

translator = GoogleTranslator(source='en', target='zh-CN')
PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class Word(object):
    def __init__(self):
        pass

    @staticmethod
    def get_word_definitions(word):
        """
        功能：查询单词词性、英文释义、中文释义
        作者：GREGORY
        修订：2025-12-13 GREGORY Created
        :param word: 查询的单词
        :return: 单词释义列表，每个元素表示一个释义，含词性、英文释义、中文释义
        """
        synsets = wn.synsets(word)
        results = []
        for syn in synsets:
            # 词性 n/v/adj/adv
            pos = syn.pos()
            # 英文释义
            definition_en = syn.definition()
            # 中文翻译
            # deep-translator 是同步的
            definition_zh = translator.translate(definition_en)
            results.append({
                "word": word,
                "pos": pos,
                "definition_en": definition_en,
                "definition_zh": definition_zh,
                "examples": syn.examples()
            })
        return results

    @staticmethod
    def get_bible_words():
        """
        功能：解析圣经全量的单词表
        作者：GREGORY
        修订：2025-12-14 GREGORY Created
        :return: 字典：圣经全量单词表
        """
        excel = os.path.join(PROJ_ROOT, 'src/data', 'bible_words_full.xlsx')
        df = pandas.read_excel(excel, sheet_name="Sheet1")
        word_dict = df.set_index("word").to_dict(orient="index")
        return word_dict

    def gen_bible_words(self, words:dict):
        """
        功能：生成圣经全量的单词表，含词性、中文释义、英文释义
        作者：GREGORY
        修订：2025-12-14 GREGORY Created
        :param words: dict 圣经全量单词表
        :return: 0 success, 1 failure
        """
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        output = os.path.join(PROJ_ROOT, "output", f"bible_words_full_{time_str}")
        print(output)
        for w in words:
            ans_list = self.get_word_definitions(w)
            print(ans_list[-1])
        return 0
