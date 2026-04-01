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
import spacy
from pathlib import Path
from collections import Counter
from nltk.corpus import wordnet as wn
from deep_translator import GoogleTranslator
from src.lib import ecdict

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
             2026-01-24 GREGORY wordnet性能差
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

    def get_bible_words(self):
        """
        功能：读取圣经全量的单词表，《bible_words_full.xlsx》由chatGPT提供，有单词勘误
        作者：GREGORY
        修订：2025-12-14 GREGORY Created
        :return: 字典：圣经全量单词表
        """
        excel = os.path.join(PROJ_ROOT, 'src/data', 'bible_words_full.xlsx')
        df = pandas.read_excel(excel, sheet_name="Sheet1")
        word_dict = df.set_index("tword").to_dict(orient="index")
        return word_dict

    def parse_bible_words(self, txt_file):
        """
        功能：解析圣经全量的单词表
        作者：GREGORY
        修订：2026-01-03 GREGORY Created
        :param txt_file: 圣经电子书绝对路径
        :return: 字典：圣经全量单词表
        """
        # 1. 加载 spaCy 英文模型
        print("spacy loading...")
        nlp = spacy.load("en_core_web_sm", disable=["ner"])
        print("spacy loaded success!")
        nlp.max_length = 5_000_000

        # 2. 读取圣经文本
        print("bible text loading...")
        txt_path = Path(txt_file)
        text = txt_path.read_text(encoding="utf-8")
        print("bible text loaded success!")

        # 3. 解析圣经文本
        word_freq = Counter()
        example_sentence = {}
        print("nlp loading...")
        doc = nlp(text)
        print("nlp loaded success!")
        for sent in doc.sents:
            sent_text = sent.text.strip()
            print(sent_text)
            for token in sent:
                # 过滤条件
                if not token.is_alpha:
                    continue

                lemma = token.lemma_.lower()

                if lemma == "":
                    continue

                # 统计词频
                word_freq[lemma] += 1

                # 保存第一条例句
                if lemma not in example_sentence:
                    example_sentence[lemma] = sent_text
        # 返回
        return word_freq, example_sentence

    def parse_bible_words_split(self, txt_file):
        """
        功能：解析圣经全量的单词表（切分文本方式），意在解决单次加载内存溢出问题
        作者：GREGORY
        修订：2026-01-19 GREGORY Created
        :param txt_file: 圣经电子书绝对路径
        :return: 字典：圣经全量单词表
        """
        word_freq = Counter()
        example_sentence = {}

        nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
        nlp.enable_pipe("senter")

        with open(txt_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                doc = nlp(line)

                for sent in doc.sents:
                    sent_text = sent.text.strip()
                    print(sent_text)
                    for token in sent:
                        if not token.is_alpha:
                            continue

                        lemma = token.lemma_.lower()
                        if not lemma:
                            continue

                        word_freq[lemma] += 1

                        if lemma not in example_sentence:
                            example_sentence[lemma] = sent_text

        return word_freq, example_sentence


    def gen_bible_words(self, words:dict):
        """
        功能：生成圣经全量的单词表，含词性、中文释义、英文释义，get_word_definitions性能差
        作者：GREGORY
        修订：2025-12-14 GREGORY Created
        :param words: dict 圣经全量单词表
        :return: 0 success, 1 failure
        """
        meaning_words = {}
        for k, v in words.items():
            ans_list = self.get_word_definitions(k)
            # 取首个释义
            first_definition = ans_list[-1]
            print(first_definition)
            v["pos"] = first_definition["pos"]
            v["definition_en"] = first_definition["definition_en"]
            v["definition_zh"] = first_definition["definition_zh"]
            meaning_words[k] = v
        return meaning_words

    def report_bible_words(self, filename:str):
        """
        功能：生成圣经全量的单词报表
        作者：GREGORY
        修订：2026-01-01 GREGORY Created
             2026-01-25 GREGORY Add phonetic field
        :param filename NIV_Bible_Full_Text.txt
        :return: 0 success, 1 failure
        """
        # 1. 定义表头
        columns = ["no.", "tword", "freq", "hold", "phonetic", "definition_en", "definition_zh", "bible_example"]

        # 2. 数据加载
        txt_bible = os.path.join(PROJ_ROOT, "src/data", filename)
        word_freq, word_example = self.parse_bible_words(txt_bible)
        print("ecdict loading...")
        word_ecdict = ecdict.load_ecdict(os.path.join(PROJ_ROOT, "src/data", "ecdict.csv"))
        print("ecdict loaded success!")

        # 3. 行容器逐行追加数据
        rows, i = [], 1
        for tword, freq in sorted(word_freq.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
            definition_en = word_ecdict.get(tword, {}).get("definition")
            definition_zh = word_ecdict.get(tword, {}).get("translation")
            phonetic = word_ecdict.get(tword, {}).get("phonetic")
            rows.append([
                i,
                tword,
                freq,
                "",
                phonetic if definition_en else "ecdict查phonetic结果为空",
                definition_en if definition_en else "ecdict查definition_en结果为空",
                definition_zh if definition_zh else "ecdict查definition_zh结果为空",
                word_example[tword]
            ])
            i = i + 1

        # 4. 生成DataFrame
        df = pandas.DataFrame(rows, columns=columns)

        # 5. 写入Excel并保存
        time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        output = os.path.join(PROJ_ROOT, "output", f"{Path(filename).stem}_{time_str}.xlsx")
        df.to_excel(output, sheet_name="Sheet1", index=False)

        print("\r\nExcel output successfully saved to {}\r\n".format(output))
        return 0


if __name__ == '__main__':
    word = Word()
    word.report_bible_words(filename="NIV_Bible_Full_Text.txt")
