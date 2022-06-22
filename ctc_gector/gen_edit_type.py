from difflib import SequenceMatcher


def gen_edit_type(source, target):
    matcher = SequenceMatcher(None, source, target)
    diffs = list(matcher.get_opcodes())
    # print(diffs)
    all_edits = []

    for diff in diffs:
        tag, i1, i2, j1, j2 = diff
        if tag == 'equal':
            for _ in range(i1, i2):
                all_edits.append(['$KEEP'])
        elif tag == 'delete':
            _temp = []
            for _ in range(i1, i2):
                _temp.append('$DELETE')
            all_edits.append(_temp)
        elif tag == 'insert':
            _temp = []
            for i in range(j2-j1):
                _temp.append(f"$APPEND_{target[j1+i:j1+i+1]}")
            all_edits.append(_temp)
        elif tag == 'replace':
            _temp = []
            for i in range(i2-i1):
                _temp.append(f"$REPLACE_{target[j1+i:j1+i+1]}")
            all_edits.append(_temp)
    edits = [y for x in all_edits for y in x]
    return edits, all_edits

def gen_edit_type_bak(source, target):
    matcher = SequenceMatcher(None, source, target)
    diffs = list(matcher.get_opcodes())
    # print(diffs)
    all_edits = []

    for diff in diffs:
        tag, i1, i2, j1, j2 = diff
        if tag == 'equal':
            for _ in range(i1, i2):
                all_edits.append('$KEEP')
        elif tag == 'delete':
            for _ in range(i1, i2):
                all_edits.append('$DELETE')
        elif tag == 'insert':
            for i in range(j2-j1):
                all_edits.append(f"$APPEND_{target[j1+i:j1+i+1]}")
        elif tag == 'replace':
            for i in range(i2-i1):
                all_edits.append(f"$REPLACE_{target[j1+i:j1+i+1]}")
    return all_edits, diffs

# def set_range(edits, diffs):
#     output = []
#     for diff in diffs:
#         tag, i1, i2, j1, j2 = diff
#         if tag == 'equal':
#             for _ in range(i1, i2):
#                 output.append(['$KEEP'])
#         if tag == 'insert':
#             _temp = []
#             for i in range(j2-j1):
#                 _temp.append()
#                 output.append(f"$APPEND_{target[j1+i:j1+i+1]}")



if __name__ == "__main__":
    source = "游泳池的平均深度"
    target = "游泳池的小明家平均深度"
    result, diffs = gen_edit_type(source, target)
    print(len(source), len(result))
    print(diffs)
    print(result)
    

