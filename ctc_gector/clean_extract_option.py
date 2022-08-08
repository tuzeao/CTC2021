import re


possible_option_tag = 'abcd1234①②③④'
num_pt = re.compile(r'\d+(\.\d+)?$')
option_num_1_pt = re.compile(r'(1)(\.)')
option_num_2_pt = re.compile(r'(2)(\.)')


def is_number(text: str):
    return num_pt.match(text)


def options_process(text: str):
    if not text:
        return '', ''
    text = text.lower()
    if '.' in text:
        split_text = text.split(".")
        first = split_text[0]
        if len(split_text) >= 2 and len(first) == 1 and first in possible_option_tag:
            return first.strip(), ''.join(split_text[1:]).strip()
    if ' ' in text:
        split_text = text.split(" ")
        first = split_text[0]
        if len(split_text) >= 2 and len(first) == 1 and first in possible_option_tag:
            return first.strip(), ''.join(split_text[1:]).strip()
    return '', text


def options_with_abcd(text: str, strict=False):
    output = []

    text = text.lower()
    begin_idx = text.rfind("a.") if strict else text.rfind("a")
    if begin_idx == -1:
        return output, text
    raw = text[begin_idx:]
    text_without_options = text[:begin_idx]
    if "b" not in raw:
        return output, text

    # 比较简单暴力的分法  根据abcd作为分隔符
    rest = raw

    def _process(char, rest):
        rest, op = rest.split(char)[0], "".join(rest.split(char)[1:])
        while True:
            op = op.strip()
            if " " in op:
                blank_idx = op.find(" ")
                start, end = op[blank_idx - 1], op[blank_idx + 1]
                if is_number(start) and is_number(end):
                    op = op.strip().replace(" ", ".", 1)
                else:
                    op = op.strip().replace(" ", "@##&", 1)
            else:
                op = op.strip().strip(".").replace("@##&", "")
                break
        output.append([char.strip().strip("."), op.strip()])
        return rest

    search_char = ['d.', 'c.', 'b.', 'a.'] if strict else ['d', 'c', 'b', 'a']

    for char in search_char:
        if char in rest:
            rest = _process(char, rest)
    return output, text_without_options

def options_with_symbol_1234(text):
    output = []

    text = text.lower()
    begin_idx = text.rfind("①")
    if begin_idx == -1:
        return output, text
    raw = text[begin_idx:]
    text_without_options = text[:begin_idx]
    if "②" not in raw:
        return output, text

    # 比较简单暴力的分法  根据abcd作为分隔符
    rest = raw

    def _process(char, rest):
        rest, op = rest.split(char)[0], "".join(rest.split(char)[1:])
        while True:
            op = op.strip()
            if " " in op:
                blank_idx = op.find(" ")
                start, end = op[blank_idx - 1], op[blank_idx + 1]
                if is_number(start) and is_number(end):
                    op = op.strip().replace(" ", ".", 1)
                else:
                    op = op.strip().replace(" ", "@##&", 1)
            else:
                op = op.strip().strip(".").replace("@##&", "")
                break
        output.append([char, op])
        return rest

    for char in ['④', '③', '②', '①']:
        if char in rest:
            rest = _process(char, rest)

    return output, text_without_options


def options_with_1234(text):
    output = []

    text = text.lower()
    if not option_num_1_pt.search(text) or not option_num_2_pt.search(text):
        return output, text

    output = []

    text = text.lower()
    begin_idx = text.rfind("1.")
    if begin_idx == -1:
        return output, text
    raw = text[begin_idx:]
    text_without_options = text[:begin_idx]
    if "2." not in raw:
        return output, text

    # 比较简单暴力的分法  根据abcd作为分隔符
    rest = raw

    def _process(char, rest):
        rest, op = rest.split(char)[0], "".join(rest.split(char)[1:])
        while True:
            op = op.strip()
            if " " in op:
                blank_idx = op.find(" ")
                start, end = op[blank_idx - 1], op[blank_idx + 1]
                if is_number(start) and is_number(end):
                    op = op.strip().replace(" ", ".", 1)
                else:
                    op = op.strip().replace(" ", "@##&", 1)
            else:
                op = op.strip().strip(".").replace("@##&", "")
                break
        output.append([char.strip("."), op])
        return rest

    for char in ['4.', '3.', '2.', '1.']:
        if char in rest:
            rest = _process(char, rest)

    return output, text_without_options


if __name__ == '__main__':
    # strs = "<p>某物质的营养成分为糖类，蛋白质、矿物质三种，糖类占一半，现在用扇形统计图来反映各营养成分的占比，表示蛋白质的扇形的面积占半圆面积的$$\frac{4}{5}$$，则表示矿物质的扇形的圆心角是（ &nbsp; ）$${}^\circ $$．</p><br/>A. <p>$$18$$</p><br/>B. <p>$$360$$</p><br/>C. <p>$$36$$</p><br/>D. <p>$$72$$</p>"
    from clean_3rd_qbody_utils import clean_html_and_to_ocr_3rd
    from clean_3rd_sql_body import clean_3rd_process

    f = open("dev_input.txt", "r", encoding="utf-8")
    for line in f:
        qbody = line.strip()
        print(clean_html_and_to_ocr_3rd(qbody))
        print(clean_3rd_process(qbody))


    # strs = [
    #     "7.21.6=4.5，里应该填(※).A.-B.\timesc.÷",
    #     "",
    #     "",
    #     "",
    #     "",
    #     "",
    #     "",
    #     "",
    #     "",
    # ]
    # for s in strs:
    #     if not s: continue
    #     print(s)
    #     clean_s = clean_html_and_to_ocr_3rd(s)
    #     print(clean_s)
    #     print(options_with_abcd(clean_s, strict=True))
    #     print(options_with_symbol_1234(clean_s))
    #     print(options_with_1234(clean_s))
    #     print("-"*50)
