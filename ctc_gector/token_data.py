from tokenization import WordpieceTokenizer, convert_to_unicode, load_vocab
from tqdm import tqdm
import argparse
import sys
import os


def main(args):
    if not os.path.exists(args.i):
        print("？")
        sys.exit()
    vocab = load_vocab("vocab.txt")
    tokenizer = WordpieceTokenizer(vocab=vocab)
    with open(args.i, "r", encoding="utf-8") as f, open(args.o, "w", encoding="utf-8") as w:
        lines = f.readlines()
        count = 0
        for line in tqdm(lines):
            line = convert_to_unicode(line)
            if not line:
                continue
            tokens = tokenizer.tokenize(line)
            line = ' '.join(tokens)
            w.write(f"{line}\n")
            count += 1
        print(f"input: {len(lines)}, output: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True)
    parser.add_argument('-o', required=True)
    args = parser.parse_args()
    main(args)





