import argparse
import os
import json
import re
import Levenshtein
import numpy as np
from tqdm import tqdm
from collections import defaultdict

from tokenization import WordpieceTokenizer, load_vocab
vocab = load_vocab("vocab.txt")
tokenizer = WordpieceTokenizer(vocab=vocab)


#convert data from parallel to tagging

SEQ_DELIMETERS = {"tokens": " ",
                  "labels": "SEPL|||SEPR",
                  "operations": "SEPL__SEPR"}


START_TOKEN = "$START"

def load_similar_zi():
    record = defaultdict(list)
    with open("data/similar_zi.txt", "r", encoding="utf8") as f:
        for l in f:
            item = l.split()
            if len(item) < 2: continue
            s1, s2 = item[:2]
            for word in s2:
                record[s1].append(word)
    return record

def load_math_keyword():
    output = set()
    with open("data/math_keywords.txt", "r", encoding="utf8") as f:
        for l in f:
            output.add(l.strip())
    return output

def load_unit():
    output = {}
    with open("data/unit_record.txt", "r", encoding="utf8") as f:
        for l in f:
            l = l.strip().split()
            output[l[0]] = l[1:]
    return output


similar_zi = load_similar_zi()
math_keyword = load_math_keyword()
units = load_unit()

def levenshtein_align(source_sent, target_sent, compress=True):
    # source_tokens = source_sent.split(' ')
    # target_tokens = target_sent.split(' ')

    source_tokens = tokenizer.tokenize(source_sent)
    target_tokens = tokenizer.tokenize(target_sent)
    source_tokens = [x.replace("##", "") for x in source_tokens]
    target_tokens = [x.replace("##", "") for x in target_tokens]

    source_tokens_with_start = ["$start"] + source_tokens
    target_tokens_with_start = ["$start"] + target_tokens

    lev = [[0] * (len(target_tokens) + 1) for _ in range(len(source_tokens) + 1)]
    ops = [[0] * (len(target_tokens) + 1) for _ in range(len(source_tokens) + 1)]
    for i in range(1, len(source_tokens) + 1):
        lev[i][0] = i
        ops[i][0] = "$DELETE"
    for j in range(1, len(target_tokens) + 1):
        lev[0][j] = j
        ops[0][j] = "$APPEND_" + target_tokens_with_start[j]
    lev[0][0] = 0
    
    for i in range(1, len(source_tokens) + 1):
        for j in range(1, len(target_tokens) + 1):
            cost1 = lev[i-1][j] + 1
            cost2 = lev[i][j-1] + 1            
            cost3 = lev[i-1][j-1] + 1 if source_tokens_with_start[i] != target_tokens_with_start[j] else lev[i-1][j-1] + 0
            transform = apply_transformation(source_tokens_with_start[i], target_tokens_with_start[j])
            cost3 = lev[i-1][j-1] if transform else lev[i-1][j-1] + 1
            if cost1 <= cost2 and cost1 <= cost3:
                lev[i][j] = cost1
                ops[i][j] = "$DELETE"
            elif cost2 <= cost1 and cost2 <= cost3:
                lev[i][j] = cost2
                ops[i][j] = "$APPEND_" + target_tokens_with_start[j]
            else:
                lev[i][j] = cost3
                if transform:
                    ops[i][j] = transform
                else:
                    ops[i][j] = "$REPLACE_" + target_tokens_with_start[j]
                # ops[i][j] = "$REPLACE_" + target_tokens_with_start[j]

    
    s = len(source_tokens)
    t = len(target_tokens)
    edits = []
    while s != 0 or t != 0:
        edits.append([(s,s+1),ops[s][t]])
        if ops[s][t].startswith("$TRANSFORM") or ops[s][t].startswith("$REPLACE") or ops[s][t].startswith("$KEEP"):            
            s = s-1
            t = t-1
        elif ops[s][t].startswith("$APPEND"):
            t = t-1
        else:
            s = s-1
    edits.reverse()

    # get labels
    labels = convert_edits_to_labels(source_tokens, edits, compress)
    # match tags to source tokens
    sent_with_tags = add_labels_to_the_tokens(source_tokens, labels)
    return sent_with_tags


def align_sequences(source_sent, target_sent, compress=True):
    source_tokens = source_sent.split()
    target_tokens = target_sent.split()
    source_tokens_with_start = ["$start"] + source_tokens
    target_tokens_with_start = ["$start"] + target_tokens

    lev = [[0] * (len(target_tokens) + 1) for _ in range(len(source_tokens) + 1)]
    ops = [[0] * (len(target_tokens) + 1) for _ in range(len(source_tokens) + 1)]
    for i in range(1, len(source_tokens) + 1):
        lev[i][0] = i
        ops[i][0] = "$DELETE"
    for j in range(1, len(target_tokens) + 1):
        lev[0][j] = j
        ops[0][j] = "$APPEND_" + target_tokens_with_start[j]
    lev[0][0] = 0

    for i in range(1, len(source_tokens) + 1):
        for j in range(1, len(target_tokens) + 1):
            cost1 = lev[i - 1][j] + 1
            cost2 = lev[i][j - 1] + 1
            cost3 = lev[i - 1][j - 1] + 1 if source_tokens_with_start[i] != target_tokens_with_start[j] else lev[i - 1][
                                                                                                                 j - 1] + 0
            transform = apply_transformation(source_tokens_with_start[i], target_tokens_with_start[j])
            cost3 = lev[i - 1][j - 1] if transform else lev[i - 1][j - 1] + 1
            if cost1 <= cost2 and cost1 <= cost3:
                lev[i][j] = cost1
                ops[i][j] = "$DELETE"
            elif cost2 <= cost1 and cost2 <= cost3:
                lev[i][j] = cost2
                ops[i][j] = "$APPEND_" + target_tokens_with_start[j]
            else:
                lev[i][j] = cost3
                if transform:
                    ops[i][j] = transform
                else:
                    ops[i][j] = "$REPLACE_" + target_tokens_with_start[j]
                # ops[i][j] = "$REPLACE_" + target_tokens_with_start[j]

    s = len(source_tokens)
    t = len(target_tokens)
    edits = []
    while s != 0 or t != 0:
        edits.append([(s, s + 1), ops[s][t]])
        if ops[s][t].startswith("$TRANSFORM") or ops[s][t].startswith("$REPLACE") or ops[s][t].startswith("$KEEP"):
            s = s - 1
            t = t - 1
        elif ops[s][t].startswith("$APPEND"):
            t = t - 1
        else:
            s = s - 1
    edits.reverse()
    # get labels
    labels = convert_edits_to_labels(source_tokens, edits, compress)
    # match tags to source tokens
    sent_with_tags = add_labels_to_the_tokens(source_tokens, labels)
    return sent_with_tags


def convert_edits_to_labels(source_tokens, edits, compress=True):
    labels = []
    for i in range(len(source_tokens) + 1):
        edit_operations = [x[1] for x in edits if x[0][0] == i and x[0][1] == i + 1]
        if len(edit_operations) > 1:
            edit_operations = [x for x in edit_operations if x != "$KEEP"]
        if not edit_operations:
            labels.append(["$KEEP"])
        else:
            labels.append(edit_operations)
    return labels


def apply_transformation(source_token, target_token):
    '''
        检查source_token与target_token是否满足大小写、单复数等的变化
    '''
    checks = [check_equal, check_number, check_similar_zi, check_unit, check_mathword]
    for check in checks:
        transform = check(source_token, target_token)
        if transform:
            return transform
    return None


def check_mathword(source, target):
    if source in math_keyword and target in math_keyword:
        return "$TRANSFORM_MATH"
    return None


def check_unit(source, target):
    if source in units.get(target, []):
        return "$TRANSFORM_UNIT"
    return None


def check_similar_zi(source, target):
    if source in similar_zi.get(target, []):
        return "$TRANSFORM_OCR"
    return None


def check_number(source_token, target_token):
    def pure_number(text):
        """判断是否是纯数字"""
        num_pt = re.compile(r'[\d零一二两三四五六七八九十百千万亿\.]+$')
        if num_pt.match(text):
            return True
        return False

    if pure_number(source_token) and pure_number(target_token):
        # return "$REPLACE_" + target_token
        return "$TRANSFORM_NUM"
    return None

def check_equal(source_token, target_token):
    if source_token == target_token:
        return "$KEEP"
    else:
        return None


def add_labels_to_the_tokens(source_tokens, labels, delimeters=SEQ_DELIMETERS):
    '''
    将token序列与label序列结合，组成序列标注的格式
    source_tokens: 不带start_token的token序列
    labels: 包含start_token的标签
    '''
    tokens_with_all_tags = []
    source_tokens_with_start = [START_TOKEN] + source_tokens
    for token, label_list in zip(source_tokens_with_start, labels): #lable_list:一个token会有多个变换
        if len(token.split(' ')) > 1:
            tokens = token.split(' ')
            for token in tokens[:-1]:
                comb_record = token + delimeters['labels'] + '$KEEP' #$transform_split标签
                tokens_with_all_tags.append(comb_record)
            token = tokens[-1]
        #解决经过convert_append_replace后导致的$REPLACE_token标签中token与原token一致的问题
        #如book->Books，原标签$REPLACE_Books，经过转换后$REPLACE_book, $transform_VERB_VBZ, $transform_CASE_CAPITAL
        #这显然是不合理的
        if len(label_list) > 1: #label_list中如果只有一个标签，无条件保留
            label = label_list[0]
            if label.startswith('$REPLACE'):
                word = label.split('_')[-1]
                if token == word:
                    label_list = label_list[1:]
        all_tags = delimeters['operations'].join(label_list)
        comb_record = token + delimeters['labels'] + all_tags
        tokens_with_all_tags.append(comb_record)
    return delimeters['tokens'].join(tokens_with_all_tags)


def change_format(text: str):
    output = []
    sp1 = text.split(" ")
    for s in sp1:
        word, ops = s.split("SEPL|||SEPR")
        ops = ops.split("SEPL__SEPR")
        _temp = []
        for op in ops:
            _temp.append([word, op])
        output.append(_temp)
    return output


def gen_edit_type(source, target):
    result = levenshtein_align(source, target)
    return change_format(result)


if __name__ == '__main__':    
    source = '小百有10个元dm'
    target = '小百有10个角m'
    # result = levenshtein_align(source, target)
    # print(change_format(result))
    # print(gen_edit_type(source, target))
    for info in gen_edit_type(source, target):
        print(info)
    #
    # print(levenshtein_align(source, target))
    # print(units)
