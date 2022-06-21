

def read(path):
    output = []
    with open(path, 'r', encoding='utf8') as f:
        for l in f:
            output.append(l.strip())
    return output

data = read("data/output_vocabulary/labels.txt")

tag_to_index = {data[i]: i for i in range(len(data))}
index_to_tag = {i: data[i] for i in range(len(data))}
