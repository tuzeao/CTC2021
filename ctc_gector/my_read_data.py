import pandas as pd
import numpy as np
import argparse
from text_utils import text_process

def main(args):
    DATA_PATH = args.i
    data = pd.read_excel(DATA_PATH, keep_default_na=False)
    df = np.array(pd.DataFrame(data)).tolist()

    with open(args.s, "w", encoding="utf-8") as fs, open(args.t, "w", encoding="utf-8") as ft:
        for info in df:
            t1, t2 = info[0], info[1]
            if "SUBQBODY" in t1 or "SUBQBODY" in t2: continue
            t1, t2 = text_process(t1), text_process(t2)
            fs.write(t2+"\n")
            ft.write(t1+"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='Path to the input file', required=True)
    parser.add_argument('-s', help='Path to the source file', required=True)
    parser.add_argument('-t', help='Path to the target file', required=True)
    args = parser.parse_args()
    main(args)




