from clean_yd_qbody_utils import clean_html_and_to_ocr_yd
from clean_trans_symbol_to_ocr import clean_label
from clean_extract_option import options_process
import json
import re
from typing import Dict


def read_qbody_txt(path):
    output = []
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.replace("\\\\\"", "'")
            line = json.loads(line)
            output.append(line)
    return output


def server_text_to_ocr(text):
    text = clean_label(text)
    # 最终去空格，符合ocr要求
    text = text.replace(' ', '')
    text = text.replace('　', '')
    text = text.replace('()', '(※)')
    return text


def get_qbody_content(qbody: Dict, fetch_all: bool = False):
    """提取sql题库数据中的文本，只提取一道题的"""
    outs = {
        'stem': '',
        'options': [],
        'sub_qbody': []
    }
    if not isinstance(qbody, dict):
        return ''
    qbody_text = qbody.get('qbody') or qbody.get('origin')
    if qbody_text:
        outs['stem'] = clean_html_and_to_ocr_yd(qbody_text)
    # if fetch_all:
    #     answer_text = ''.join([clean_html_and_to_ocr_yd(ans) for ans in qbody.get('answers', [])])
    #     if answer_text:
    #         outs.append(answer_text)
    option_text = [clean_html_and_to_ocr_yd(opt) for opt in qbody.get('options', [])]
    if option_text:
        outs['options'].extend(option_text)
    for subQbody in qbody.get('subQbody',[]):
        sub_qbody = get_qbody_content(subQbody, fetch_all=fetch_all)
        if sub_qbody:
            outs['sub_qbody'].append(sub_qbody)
    return outs

def reformat_output(data):
    # 1. 处理options
    options = data['options']
    new_options = []
    for op in options:
        new_options.append(options_process(op))
    data['options'] = new_options

    # 2. 有多子题（sub_qbody）无options把文本拼起来
    stem, options, sub_qbody = data['stem'], data['options'], data['sub_qbody']
    if not options:
        for sub_q in sub_qbody:
            if sub_q['options']: break
        else:
            sub_stem = "".join([x['stem'] for x in sub_qbody])
            stem += sub_stem
            data['stem'], data['options'], data['sub_qbody'] = stem, options, []

    return data

def clean_yd_process(qbody):
    result = get_qbody_content(qbody)
    result = reformat_output(result)
    return result

if __name__ == '__main__':
    path = "C:\\Users\\tuza\\projects\\CTC2021\\ctc_gector\\inputs\\youdao_tiku_mysql"
    qbodys = read_qbody_txt(path)
    qbodys = qbodys[:500]
    for idx, qbody in enumerate(qbodys):
        # print(qbody)
        # result = get_qbody_content(qbody)
        # print(result)
        # print(clean_label(result[0]))
        if idx in [262, 257, 254]:
            print(qbody)
        # print(idx, reformat_output(result))
        # print(idx, reformat_output(result))
        print(clean_yd_process(qbody))

    # s = "<p>照样子看图圈数。</p><p><img class='_img_block' src='https://nos.netease.com/yd-searchq/a9ca7c94-2238-4d1b-bfdb-3ad5c3f2e93e.png' title='1651369779278.png' alt='image.png' width='500' height='109.10404624277457' style='width:500px;height:109.10404624277457px;'/></p>"
    # print(clean_qbody_text(s))

    # data = {'stem': '看图填空。', 'options': [], 'sub_qbody': [{'stem': '从上往下数，欢欢的蛋糕放在第1层的下面，第3层的上面，他的蛋糕放在第(※)层。', 'options': [], 'sub_qbody': []}, {'stem': '从下往上数，第(※)层放的蛋糕最多，第(※)层一块蛋糕也没有。', 'options': [], 'sub_qbody': []}]}

    # print(reformat_output(data))
