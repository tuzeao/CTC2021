import sys
sys.path.append(".")
import argparse
from tqdm import tqdm
from edit_align import align_sequences
from helpers import write_lines, read_parallel_lines



def convert_data_from_raw_files(source_file, target_file, output_file, chunk_size, max_len):
    skipped = 0
    tagged = []
    source_data, target_data = read_parallel_lines(source_file, target_file)
    print(f"The size of raw dataset is {len(source_data)}")
    cnt_total, cnt_all, cnt_tp = 0, 0, 0
    for source_sent, target_sent in tqdm(zip(source_data, target_data)):
        if len(source_sent.split()) > max_len:
            skipped += 1
            continue
        try:
            aligned_sent = align_sequences(source_sent, target_sent)
        except Exception:
            aligned_sent = align_sequences(source_sent, target_sent)
        if source_sent != target_sent:
            cnt_tp += 1
        alignments = [aligned_sent]
        cnt_all += len(alignments)

        if alignments:
            cnt_total += len(alignments)
            tagged.extend(alignments)
        if len(tagged) > chunk_size:
            write_lines(output_file, tagged, mode='a')
            tagged = []

    print(f"Overall extracted {cnt_total}. "
          f"Original TP {cnt_tp}."
          f" Original TN {cnt_all - cnt_tp}")
    skipped_rate = skipped / len(source_data)
    print(f"Skipped rate:", skipped_rate)
    if tagged:
        write_lines(output_file, tagged, 'a')




def main(args):
    convert_data_from_raw_files(args.source, args.target, args.output_file, args.chunk_size, args.max_len)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source',
                        help='Path to the source file',
                        required=True)
    parser.add_argument('-t', '--target',
                        help='Path to the target file',
                        required=True)
    parser.add_argument('-o', '--output_file',
                        help='Path to the output file',
                        required=True)
    parser.add_argument('--chunk_size',
                        type=int,
                        help='Dump each chunk size.',
                        default=1000000)

    parser.add_argument('-m', '--max_len',
                        type=int,
                        help='max sentence length',
                        default=128)

    args = parser.parse_args()
    main(args)
