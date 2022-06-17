import pandas as pd
import numpy as np
import argparse


def main(args):
    DATA_PATH = args.i
    data = pd.read_excel(DATA_PATH, keep_default_na=False)
    df = np.array(pd.DataFrame(data)).tolist()

    with open(args.s, "w", encoding="utf-8") as fs, open(args.t, "w", encoding="utf-8") as ft:
        for info in df:
            t1, t2 = info[0], info[1]
            fs.write(t1+"\n")
            ft.write(t1+"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='Path to the input file', required=True)
    parser.add_argument('-s', help='Path to the source file', required=True)
    parser.add_argument('-t', help='Path to the target file', required=True)
    args = parser.parse_args()
    main(args)




