#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =====================================================
#  Copyright (c) 2026 GREGORY
#  Description : ecdict.py
#  Author      : weiguoxian@gmail.com
#  Created     : 2026-01-01
#  License     : MIT License
# =====================================================
import csv


def load_ecdict(path):
    word_ecdict = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row["word"]
            word_ecdict[word] = row
    return word_ecdict