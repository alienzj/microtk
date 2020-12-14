mod utils;

use bio::io::{fasta, fastq};
use clap::{App, Arg, SubCommand};
use niffler;
use std::io;

fn main() {
    let matches = App::new("microtk")
        .version("0.1")
        .author("alienzj <alienchuj@gmail.com>")
        .about("a micro toolkit for bioinformatics")
        .subcommand(
            SubCommand::with_name("len")
                .about("compute length for each record of fasta/fastq file")
                .arg(
                    Arg::with_name("input-file")
                        .short("i")
                        .required(true)
                        .value_name("FILE"),
                ),
        )
        .subcommand(
            SubCommand::with_name("fastx-header")
                .about("compute length for each record of fasta/fastq file")
                .arg(
                    Arg::with_name("--input")
                        .short("i")
                        .required(true)
                        .value_name("FILE"),
                )
                .arg(
                    Arg::with_name("--output")
                        .short("o")
                        .required(false)
                        .value_name("FILE")
                        .default_value("-"),
                ),
        )
        .subcommand(
            SubCommand::with_name("fastx-fixer")
                .about("compute length for each record of fasta/fastq file")
                .arg(
                    Arg::with_name("--input")
                        .short("i")
                        .required(true)
                        .value_name("FILE"),
                )
                .arg(
                    Arg::with_name("--output")
                        .short("o")
                        .required(false)
                        .value_name("FILE")
                        .default_value("-"),
                ),
        )
        .get_matches();

    if let Some(matches) = matches.subcommand_matches("fastx-header") {
        utils::fastx_header(
            matches.value_of("input").unwrap(),
            matches.value_of("output").unwrap(),
        );
    }
}
