#!/usr/bin/env python3

import argparse
import os

import pandas as pd
import requests
from tqdm import tqdm

PROXIES = {
    "http": "http://127.0.0.1:9910",
    "https": "http://127.0.0.1:9910",
}

ASSEMBLY_REPORT = {
    "refseq_archaea": "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/archaea/assembly_summary.txt",
    "refseq_bacteria": "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt",
    "refseq_fungi": "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/fungi/assembly_summary.txt",
    "refseq_viral": "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/viral/assembly_summary.txt",
    "genbank_archaea": "https://ftp.ncbi.nlm.nih.gov/genomes/genbank/archaea/assembly_summary.txt",
    "genbank_bacteria": "https://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt",
    "genbank_fungi": "https://ftp.ncbi.nlm.nih.gov/genomes/genbank/fungi/assembly_summary.txt",
    "genbank_viral": "https://ftp.ncbi.nlm.nih.gov/genomes/genbank/viral/assembly_summary.txt",
}


def download(report_link, outfile):
    response = requests.get(report_link, stream=True, proxies=PROXIES)

    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(
        total=total_size, unit_scale=True, desc=os.path.basename(outfile)
    )

    with open(outfile, "wb") as fout:
        for data in response.iter_content(block_size):
            if data:
                progress_bar.update(len(data))
                fout.write(data)

    progress_bar.close()


def setpath(row):
    base_name = os.path.basename(row["ftp_path"]) + "_genomic.fna.gz"
    dir_name = "/".join([PUB_PATH]) + row["ftp_path"].split("/")[3:]
    return os.path.join(dir_name, base_name)

def exists(row):
    if os.path.exists(row["local_path"]):
        return 1
    else:
        return 0

def parse(summary_txt, database, domain, set_path=False, check_exists=False):
    if not os.path.exists(summary_txt):
        print("%s is not exists, please check it" % summary_txt)
   

def main():
    parser = argparse.ArgumentParser(description="CAMISIM taxonomy generator")
    parser.add_argument("-o", "--outdir", dest="outdir", help="output directory")
    args = parser.parse_args()

    for i in ASSEMBLY_REPORT:
        download(
            ASSEMBLY_REPORT[i],
            os.path.join(args.outdir, "assembly_summary_" + i + ".txt"),
        )


if __name__ == "__main__":
    main()
