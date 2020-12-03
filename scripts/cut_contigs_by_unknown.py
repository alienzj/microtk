#!/usr/bin/env python

from Bio import SeqIO
import os
import gzip
import argparse


def cut_with_unknown(file_path, num, base, output_1, output_2):
    tag = base * num

    if file_path.endswith(".gz"):
        handle = gzip.open(file_path)
    else:
        handle = open(file_path)

    with open(output_1, "w") as oh1, open(output_2, "w") as oh2:
        for record in SeqIO.parse(handle, "fasta"):
            if tag in record.seq:
                SeqIO.write(record, oh2, "fasta")
            else:
                SeqIO.write(record, oh1, "fasta")


def main():
    parser = argparse.ArgumentParser(description="contigs filter")
    parser.add_argument(
        "--contigs", type=str, help="input contigs, format: FASTA", required=True
    )
    parser.add_argument(
        "--contigs-out-good",
        dest="contigs_out_good",
        type=str,
        help="output good contigs, format: FASTA",
    )
    parser.add_argument(
        "--contigs-out-bad",
        dest="contigs_out_bad",
        type=str,
        help="output bad contigs, format: FASTA",
    )
    parser.add_argument("--base", type=str, default="N", help="unknown base")
    parser.add_argument("--num", type=int, default=10, help="unknown base number")
    args = parser.parse_args()

    cut_with_unknown(
        args.contigs, args.num, args.base, args.contigs_out_good, args.contigs_out_bad
    )


if __name__ == "__main__":
    main()
