#!/usr/bin/env python3

import argparse
import os
from pprint import pprint

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

PUB_PATH = "/hwfssz1/pub/database/ftp.ncbi.nih.gov"


def download(session, report_link, outfile):
    with session.get(
        report_link, stream=True, proxies=PROXIES, headers={"Accept-Encoding": None}
    ) as response:
        total_size = int(response.headers.get("content-length", 0))

        if os.path.exists(outfile) and (os.path.getsize(outfile) == total_size):
            print(f"{outfile} exists, pass")
        else:
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


def setpath(row, pub_path):
    base_name = os.path.basename(row["ftp_path"]) + "_genomic.fna.gz"
    dir_name = "/".join([pub_path] + row["ftp_path"].split("/")[3:])
    return os.path.join(dir_name, base_name)


def exists(row):
    if os.path.exists(row["local_path"]):
        return 1
    else:
        return 0


def parse(summary_txt, database, domain, pub_path, set_path=False, check_exists=False):
    if not os.path.exists(summary_txt):
        print("%s is not exists, please check it" % summary_txt)
    df = (
        pd.read_csv(summary_txt, skiprows=1, sep="\t", low_memory=False)
        .astype({"ftp_path": str})
        .assign(database=database, domain=domain)
    )

    if set_path:
        df["local_path"] = df.apply(lambda x: setpath(x, pub_path), axis=1)
        if check_exists:
            df["fna_exists"] = df.apply(lambda x: exists(x), axis=1)
    return df


def main():
    parser = argparse.ArgumentParser(description="CAMISIM taxonomy generator")
    parser.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        type=str,
        required=True,
        help="output directory",
    )
    parser.add_argument(
        "-p",
        "--pub-path",
        dest="pub_path",
        type=str,
        default=PUB_PATH,
        help=f"local public database for NCBI database mirror: {PUB_PATH}",
    )
    parser.add_argument(
        "-c",
        "--check-exists",
        dest="check_exists",
        action="store_true",
        default=False,
        help=f"check whether the genome exists in the local public database: {PUB_PATH}",
    )
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    with requests.Session() as session:
        for i in ASSEMBLY_REPORT:
            summary_txt = os.path.join(args.outdir, "assembly_summary_" + i + ".txt")

            download(session, ASSEMBLY_REPORT[i], summary_txt)

            df = parse(
                summary_txt,
                i.split("_")[0],
                i.split("_")[1],
                args.pub_path,
                set_path=True,
                check_exists=args.check_exists,
            )
            df.to_csv(
                os.path.join(args.outdir, "assembly_summary_" + i + ".tsv"),
                sep="\t",
                index=False,
            )


if __name__ == "__main__":
    main()
