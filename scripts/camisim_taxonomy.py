#!/usr/bin/env python3

import os

import requests
from tqdm import tqdm

ASSEMBLIY_REPORT = [
    "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/archaea/assembly_summary.txt",
    "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt",
    "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/fungi/assembly_summary.txt",
    "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/viral/assembly_summary.txt",
    "https://ftp.ncbi.nlm.nih.gov/genomes/genbank/archaea/assembly_summary.txt",
    "https://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt",
    "https://ftp.ncbi.nlm.nih.gov/genomes/genbank/fungi/assembly_summary.txt",
    "https://ftp.ncbi.nlm.nih.gov/genomes/genbank/viral/assembly_summary.txt",
]


for report_link in ASSEMBLY_REPORT:
    response = requests.get(report_link, stream=True)
    with tqdm.wrapattr(open(os.devnull, "wb"), "write",
                       miniters=1, desc==report.split("/")[-1]) as fout:
        for chunk in
