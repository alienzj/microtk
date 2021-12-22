#!/usr/bin/env python3

import numpy as np
import gzip
import itertools
import sys


# ref qiime2
def read_fastq_seqs(filepath, phred_offset):
    # This function is adapted from @jairideout's SO post:
    # http://stackoverflow.com/a/39302117/3424666
    fh = gzip.open(filepath, "rb")
    for seq_header, seq, qual_header, qual in itertools.zip_longest(*[fh] * 4):
        qual = qual.strip()
        qual_parsed = np.frombuffer(memoryview(qual), dtype=np.uint8)
        qual_parsed = qual_parsed - phred_offset
        yield (seq_header.strip(), seq.strip(), qual_header.strip(), qual, qual_parsed)


def main():
    count = 0
    for seq_header, seq, qual_header, qual, qual_parsed in read_fastq_seqs(
        sys.argv[1], np.uint8(sys.argv[2])
    ):
        count += 1
        print(f"Seq {count} length {len(seq)}:\n{seq_header}")
        print(f"Seq:\n{seq}")
        print(f"Qual:\n{qual}")
        print(f"Qual_parsed:\n{qual_parsed}")
        print(f"Mean qual: {np.mean(qual_parsed)}\n")


if __name__ == "__main__":
    main()
