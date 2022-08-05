from clean_trans_symbol_to_ocr import clean_label
from clean_extract_option import options_process
import json
import re
from typing import Dict


FRAC_pt_all = re.compile(r'frac \d+ \d+')
FRAC_pt = re.compile(r'frac (\d+) (\d+)')

def clean_qbody_text(text):
    """提取sql题库数据中的文本，只提取一道题的"""
    import re
    def process_sql_latex(sql_text):
        img_latex_pt = re.compile(r"<img.*?data-latex=\"\\\\(.*?)\"/>")
        m = img_latex_pt.search(sql_text)
        while m is not None:
            latex = m.group(1)
            sql_text = re.sub(img_latex_pt, ' ' + latex + ' ', sql_text)
            m = img_latex_pt.search(sql_text)
        return sql_text

    def preprocess_sql(sql_text):
        """处理sql中的录题数据"""
        if not sql_text: return ""
        # if len(sql_text) > 160 or len(sql_text) < 8: return ""

        text = str(sql_text).strip()
        text = text.replace("\n", "")

        text = process_sql_latex(text)

        img_pt = re.compile(r"<img.*?>")
        div_pt = re.compile(r"<div.*?>")
        pstyle_pt = re.compile(r"<p style.*?>")
        span_pt = re.compile(r"<span.*?>")
        p1 = re.compile(r"<p.*?>")
        p2 = re.compile(r"<label.*?/label>")
        p3 = re.compile(r"<input.*?>")
        p4 = re.compile(r"<blk.*?/blk>")
        p5 = re.compile(r"<table.*?>")
        p6 = re.compile(r"<ul.*?>")
        p7 = re.compile(r"<li.*?/li>")
        p8 = re.compile(r"<td.*?>")
        p9 = re.compile(r"<em.*?>")
        p10 = re.compile(r"<dl.*?>")
        p11 = re.compile(r"<dl.*?>")
        p12 = re.compile(r"<.*?>")

        replace_pts = [img_pt, div_pt, pstyle_pt, span_pt, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]
        replace_symbs = ['<p>', '</p>', '</div>', '</span>', '&quot;', '&nbsp;', '<br/>',
                         '</td>', '</tr>', '</tbody>', '</table>', '<br>', '<tbody>',
                         '<tr>', '<td>', '<li>', '</li>', '</ul>', '<ul>', '<u>', '</u>',
                         '<sup>', '</sup>', '$', '\\t', '</em>', '<dd>', '</dd>', '</dl>',
                         '>>>>', '>>>', '<<<', '<<<<']

        for pt in replace_pts:
            text = re.sub(pt, ' ', text)

        for symb in replace_symbs:
            text = text.replace(symb, '')
        text = ' '.join(text.split())
        return text

    return preprocess_sql(text)

def read_qbody_txt(path):
    output = []
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.replace("\\\\\"", "'")
            line = json.loads(line)
            output.append(line)
    return output

def clean_some_latex(text):
    text = text.replace('&gt;', '>')
    text = text.replace('&lt;', '<')
    text = text.replace(' square ', '※')
    text = text.replace(' div ', '÷')
    text = text.replace(' times ', '×')
    text = text.replace(' quad ', ' ')
    text = text.replace(' geq ', '≥')
    text = text.replace(' leq ', '≤')

    def _frac_replace(text):
        m = FRAC_pt_all.findall(text)
        for frac_text in m:
            num = FRAC_pt.search(frac_text)
            d1, d2 = num.group(1), num.group(2)
            new_frac = "\\frac{%s}{%s}" % (d1, d2)
            text = text.replace(frac_text, new_frac)
        return text
    text = _frac_replace(text)


    return text

def clean_html_and_to_ocr(text):
    text = clean_qbody_text(text)
    text = clean_some_latex(text)
    text = clean_label(text)
    # 最终去空格，符合ocr要求
    text = text.replace(' ', '')
    text = text.replace('　', '')
    text = text.replace('()', '(※)')

    return text

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
        outs['stem'] = clean_html_and_to_ocr(qbody_text)
    if fetch_all:
        answer_text = ''.join([clean_html_and_to_ocr(ans) for ans in qbody.get('answers', [])])
        if answer_text:
            outs.append(answer_text)
    option_text = [clean_html_and_to_ocr(opt) for opt in qbody.get('options', [])]
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

def sql_qbody_process(qbody):
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
        print(sql_qbody_process(qbody))

    # s = "<p>照样子看图圈数。</p><p><img class='_img_block' src='https://nos.netease.com/yd-searchq/a9ca7c94-2238-4d1b-bfdb-3ad5c3f2e93e.png' title='1651369779278.png' alt='image.png' width='500' height='109.10404624277457' style='width:500px;height:109.10404624277457px;'/></p>"
    # print(clean_qbody_text(s))

    # data = {'stem': '看图填空。', 'options': [], 'sub_qbody': [{'stem': '从上往下数，欢欢的蛋糕放在第1层的下面，第3层的上面，他的蛋糕放在第(※)层。', 'options': [], 'sub_qbody': []}, {'stem': '从下往上数，第(※)层放的蛋糕最多，第(※)层一块蛋糕也没有。', 'options': [], 'sub_qbody': []}]}

    # print(reformat_output(data))
