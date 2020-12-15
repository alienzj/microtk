mod utils;

use bio::io::{fasta, fastq};
use clap::{App, Arg};
use niffler;
use std::io;

fn main() {
    let matches = App::new("microtk")
        .version("0.1")
        .author("alienzj <alienchuj@gmail.com>")
        .about("a micro toolkit for bioinformatics")
        //.license"GPLV3")
        .subcommand(
            App::new("len")
                .about("compute length for each record of fasta/fastq file")
                .arg(
                    Arg::new("input")
                        .short('i')
                        .required(true)
                        .value_name("FILE"),
                ),
        )
        .subcommand(
            App::new("fastx-header")
                .about("compute length for each record of fasta/fastq file")
                .arg(
                    Arg::new("input")
                        .short('i')
                        .required(true)
                        .value_name("FILE"),
                )
                .arg(
                    Arg::new("output")
                        .short('o')
                        .required(false)
                        .value_name("FILE")
                        .default_value("-"),
                ),
        )
        .subcommand(
            App::new("fastx-fixer")
                .about("compute length for each record of fasta/fastq file")
                .arg(
                    Arg::new("input")
                        .short('i')
                        .required(true)
                        .value_name("FILE"),
                )
                .arg(
                    Arg::new("output")
                        .short('o')
                        .required(false)
                        .value_name("FILE")
                        .default_value("-"),
                ),
        )
        .get_matches();

    if let Some(ref matches) = matches.subcommand_matches("fastx-header") {
        utils::fastx_header(
            matches.value_of("input").unwrap(),
            matches.value_of("output").unwrap(),
        );
    }
}
