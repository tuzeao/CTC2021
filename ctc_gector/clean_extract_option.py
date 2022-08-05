import re


possible_option_tag = 'abcd1234①②③④'
num_pt = re.compile(r'\d+(\.\d+)?$')


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


def options_with_abcd(text: str):
    output = dict()

    text = text.lower()
    begin_idx = text.rfind("a")
    if begin_idx == -1:
        return output
    raw = text[begin_idx:]
    if "b" not in raw:
        return output

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
                op = op.strip().replace("@##&", "")
                break
        output[char] = op
        return rest

    for char in ['d', 'c', 'b', 'a']:
        if char in rest:
            rest = _process(char, rest)

    return output

def options_with_1234(text):
    text = text.lower()
    # 最简单的情况: 1.haha 2. hihi
    pass

if __name__ == '__main__':
    strs = ["1. haha", "2 a", "a 3", "b. 4", "c 05", "2022"]
    for s in strs:
        print(options_process(s))


