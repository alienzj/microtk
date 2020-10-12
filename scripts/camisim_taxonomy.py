#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import requests
from tqdm import tqdm

from logbook import Logger, StreamHandler, FileHandler
import logbook
import sys


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


def download(log, session, report_link, outfile):
    with session.get(
        report_link, stream=True, headers={"Accept-Encoding": None}
    ) as response:
        remote_size = int(response.headers.get("content-length", 0))
        log.info(f"requests get {report_link} remote size: {remote_size}")

        if os.path.exists(outfile):
            local_size = os.path.getsize(outfile)
            log.notice(f"{outfile} exists, local size: {local_size}")
            if local_size == remote_size:
                log.notice(f"{outfile} local size equal to remote size, pass")
                return
            else:
                log.notice(
                    f"{outfile} local size not equal to remote size, downloading"
                )
        block_size = 4096
        progress_bar = tqdm(
            total=remote_size, unit_scale=True, desc=os.path.basename(outfile)
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


def parse(
    log, summary_txt, database, domain, pub_path, set_path=False, check_exists=False
):
    if not os.path.exists(summary_txt):
        log.warning("%s is not exists, please check it" % summary_txt)

    log.info(f"reading {summary_txt} to data frame")
    df = (
        pd.read_csv(summary_txt, skiprows=1, sep="\t", low_memory=False)
        .astype({"ftp_path": str})
        .assign(database=database, domain=domain)
    )

    if set_path:
        log.info("set local path")
        df["local_path"] = df.apply(lambda x: setpath(x, pub_path), axis=1)
        if check_exists:
            log.info("check local fna exists, be patient")
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

    logfile = os.path.join(args.outdir, "camisim_taxonomy.log")
    StreamHandler(sys.stdout, level="DEBUG").push_application()
    FileHandler(logfile, bubble=True, level="INFO").push_application()

    log = Logger("camisim_taxonomy")
    log.info(f"log recorded in {logfile}")

    df_list = []
    with requests.Session() as session:
        for i in ASSEMBLY_REPORT:
            summary_txt = os.path.join(args.outdir, "assembly_summary_" + i + ".txt")
            summary_tsv = os.path.join(args.outdir, "assembly_summary_" + i + ".tsv")

            log.info("######################################")
            log.info(f"download begin: {ASSEMBLY_REPORT[i]}")
            download(log, session, ASSEMBLY_REPORT[i], summary_txt)
            log.info(f"download end: {ASSEMBLY_REPORT[i]}")

            log.info(f"parsing begin: {summary_txt}")
            df = parse(
                log,
                summary_txt,
                i.split("_")[0],
                i.split("_")[1],
                args.pub_path,
                set_path=True,
                check_exists=args.check_exists,
            )
            log.info(f"parsing end: {summary_txt}")

            log.info(f"save {summary_txt} to {summary_tsv}")
            df.to_csv(
                summary_tsv,
                sep="\t",
                index=False,
            )
            df_list.append(df)

    df_ = pd.concat(df_list, ignore_index=True)
    log.info(
        f"concate the archaea, bacteria, fungi and viral info of refseq and genbank to one tsv"
    )
    df_.to_csv(
        os.path.join(
            args.outdir,
            "assembly_summary_refseq_genbank_archaea_bacteria_fungi_viral.tsv",
        ),
        sep="\t",
        index=False,
    )

    df_["local_path_dirname"] = df_.apply(
        lambda x: os.path.dirname(x["local_path"]), axis=1
    )

    df_.query('assembly_level == "Complete Genome" && database == "refseq"').loc[
        :, ["taxid", "organism_name", "local_path_dirname"]
    ].to_csv(
        os.path.join(args.outdir, "assembly_summary_refseq_complete_genomes.tsv"),
        sep="\t",
        index=False,
        header=None,
    )
    df_.query('assembly_level == "Chromosome" && database == "refseq"').loc[
        :, ["taxid", "organism_name", "local_path_dirname"]
    ].to_csv(
        os.path.join(args.outdir, "assembly_summary_refseq_chromosome.tsv"),
        sep="\t",
        index=False,
        header=None,
    )
    df_.query('assembly_level == "Scaffold" && database == "refseq"').loc[
        :, ["taxid", "organism_name", "local_path_dirname"]
    ].to_csv(
        os.path.join(args.outdir, "assembly_summary_refseq_scaffold.tsv"),
        sep="\t",
        index=False,
        header=None,
    )
    df_.query('assembly_level == "Contig" && database == "refseq"').loc[
        :, ["taxid", "organism_name", "local_path_dirname"]
    ].to_csv(
        os.path.join(args.outdir, "assembly_summary_refseq_contig.tsv"),
        sep="\t",
        index=False,
        header=None,
    )

    df_.query('assembly_level == "Complete Genome" && database == "genbank"').loc[
        :, ["taxid", "organism_name", "local_path_dirname"]
    ].to_csv(
        os.path.join(args.outdir, "assembly_summary_genbank_complete_genomes.tsv"),
        sep="\t",
        index=False,
        header=None,
    )
    df_.query('assembly_level == "Chromosome" && database == "genbank"').loc[
        :, ["taxid", "organism_name", "local_path_dirname"]
    ].to_csv(
        os.path.join(args.outdir, "assembly_summary_genbank_chromosome.tsv"),
        sep="\t",
        index=False,
        header=None,
    )
    df_.query('assembly_level == "Scaffold" && database == "genbank"').loc[
        :, ["taxid", "organism_name", "local_path_dirname"]
    ].to_csv(
        os.path.join(args.outdir, "assembly_summary_genbank_scaffold.tsv"),
        sep="\t",
        index=False,
        header=None,
    )
    df_.query('assembly_level == "Contig" && database == "genbank"').loc[
        :, ["taxid", "organism_name", "local_path_dirname"]
    ].to_csv(
        os.path.join(args.outdir, "assembly_summary_genbank_contig.tsv"),
        sep="\t",
        index=False,
        header=None,
    )

    log.info("done")


if __name__ == "__main__":
    main()
