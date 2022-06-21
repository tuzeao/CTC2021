from difflib import SequenceMatcher


source = "小明有5个苹果"
target = "小萌萌有5个苹果"
def gen_edit_type(source, target):
    matcher = SequenceMatcher(None, source, target)
    diffs = list(matcher.get_opcodes())
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
                all_edits.append(f"$APPEND_{target[j1:j1+i+1]}")
        elif tag == 'replace':
            for i in range(i2-i1):
                all_edits.append(f"$REPLACE_{target[j1:j1+i+1]}")
    return all_edits

# print(diffs)
# for s, edit in zip(source, all_edits):
#     print(f"{s}: {edit}")
#
# print(all_edits)


