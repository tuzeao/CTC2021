from tokenization import WordpieceTokenizer, convert_to_unicode, load_vocab
from text_utils import text_process
from tqdm import tqdm
import argparse
import sys
import os


def main(args):
    if not os.path.exists(args.s) or not os.path.exists(args.t):
        print("？")
        sys.exit()
    vocab = load_vocab("vocab.txt")
    tokenizer = WordpieceTokenizer(vocab=vocab)
    with open(args.s, "r", encoding="utf-8") as fs, open(args.t, "r", encoding="utf-8") as ft, \
            open(args.so, "w", encoding="utf-8") as ws, open(args.to, "w", encoding="utf-8") as wt:
        source_lines = fs.readlines()
        target_lines = ft.readlines()
        count = 0
        for s, t in tqdm(zip(source_lines, target_lines)):
            s = convert_to_unicode(s).strip().replace("\t", "")
            t = convert_to_unicode(t).strip().replace("\t", "")
            s, t = text_process(s), text_process(t)

            if not s or not t:
                continue
            s_tokens = tokenizer.tokenize(s)
            t_tokens = tokenizer.tokenize(t)
            if len(s_tokens) <= 3 or len(t_tokens) <= 3: continue

            s_line = ' '.join(s_tokens)
            t_line = ' '.join(t_tokens)
            s_line = s_line.replace("##", "")
            t_line = t_line.replace("##", "")
            ws.write(f"{s_line}\n")
            wt.write(f"{t_line}\n")
            count += 1
        print(f"input: {len(source_lines)}, output: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', required=True)
    parser.add_argument('-t', required=True)
    parser.add_argument('-so', required=True)
    parser.add_argument('-to', required=True)
    args = parser.parse_args()
    main(args)





