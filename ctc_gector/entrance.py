from tokenization import WordpieceTokenizer, convert_to_unicode, load_vocab
from gector.my_gec_model import GecBERTModel
from tag_index import index_to_tag, tag_to_index
# from gen_edit_type import gen_edit_type
from edit_align import gen_edit_type
import torch
import json

# ------------------- init --------------------------------------
model = GecBERTModel(vocab_path='data/output_vocabulary/',
                     model_paths=['bert_wwm/best.th'],
                     max_len=50,
                     min_len=3,
                     iterations=3,
                     min_error_probability=0.0,
                     min_probability=0.0,
                     lowercase_tokens=0,
                     model_name='bert_wwm',
                     special_tokens_fix=0,
                     log=False,
                     confidence=0.0,
                     is_ensemble=0,
                     weigths=None)
vocab = load_vocab("vocab.txt")
tokenizer = WordpieceTokenizer(vocab=vocab)



def tokenize(query):
    tokens = tokenizer.tokenize(query)
    line = ' '.join(tokens)
    return line


def _gector_predict_single(query, model):
    batch = []
    batch.append(query.split())
    all_probs = model.handle_batch(batch)
    return all_probs


def gector_predict_single(source, target):
    output = {
        "version": "20220622",
        "source": source,
        "target": target,
        "info": []
    }
    source, target = source.replace(" ", ""), target.replace(" ", "")

    source_tok, target_tok = tokenize(source), tokenize(target)
    probs = _gector_predict_single(source_tok, model)
    edits = gen_edit_type(source, target)
    # edits_index = [tag_to_index.get(e, 16501) for e in edits]
    probs = probs[0, :, :]
    max_val, max_idx = torch.max(probs, dim=-1)
    max_val, max_idx = max_val.tolist(), max_idx.tolist()

    i = 0
    while i < len(edits):
        for edit in edits[i]:
            word, edit_op = edit[:2]
            edit_idx = tag_to_index.get(edit_op, tag_to_index['@@UNKNOWN@@'])
            edit_prob = probs[i, edit_idx].tolist()
            max_id = max_idx[i]
            max_op = index_to_tag.get(max_id, 'Not Found Tag')
            max_prob = max_val[i]

            temp = {}
            temp['word'] = word
            temp['edit_op'] = edit_op
            temp['edit_idx'] = edit_idx
            temp['edit_prob'] = edit_prob
            temp['max_op'] = max_op
            temp['max_idx'] = max_id
            temp['max_prob'] = max_prob

            output['info'].append(temp)

        i += 1

    # for i in range(len(source)):
    #     word = source[i]
    #     edit_op = edits[i]
    #     edit_idx = edits_index[i]
    #     edit_prob = probs[i, edit_idx].tolist()
    #     max_id = max_idx[i]
    #     max_op = index_to_tag.get(max_id, '@@UNKNOWN@@')
    #     max_prob = max_val[i]
    #
    #     temp = {}
    #     temp['word'] = word
    #     temp['edit_op'] = edit_op
    #     temp['edit_idx'] = edit_idx
    #     temp['edit_prob'] = edit_prob
    #     temp['max_op'] = max_op
    #     temp['max_idx'] = max_id
    #     temp['max_prob'] = max_prob
    #
    #     output['info'].append(temp)

    return output

if __name__ == "__main__":
    source = "小明有5个苹果"
    target = "小明家有5个苹果"
    result = gector_predict_single(source, target)
    print(json.dumps(result, ensure_ascii=False, indent=4))
















