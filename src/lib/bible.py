#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =====================================================
#  Copyright (c) 2025 GREGORY
#  Description : bible.py
#  Author      : weiguoxian@gmail.com
#  Created     : 2025-12-13
#  License     : MIT License
# =====================================================
from nltk.corpus import wordnet as wn
from deep_translator import GoogleTranslator

# 如果第一次使用，取消注释下载 WordNet
# import nltk
# nltk.download('wordnet')
# nltk.download('omw-1.4')

translator = GoogleTranslator(source='en', target='zh-CN')


class Words(object):
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