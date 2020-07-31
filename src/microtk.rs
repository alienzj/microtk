use bio::io::{fasta, fastq};
use clap::{App, Arg, SubCommand};
use niffler;
use std::io;

fn main() -> Result<(), niffler::error::Error> {
    let matches = App::new("microtk")
        .version("0.1")
        .author("alienzj <alienchuj@gmail.com>")
        .about("a micro toolkit for microbiology")
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
        .get_matches();

    match matches.subcommand() {
        ("len", Some(m)) => len(m.value_of("input-file").unwrap()),
        _ => Ok(()),
    }
}

enum Reader<R: io::Read> {
    FASTA(fasta::Reader<R>),
    FASTQ(fastq::Reader<R>),
}

fn len(file_name: &str) -> Result<(), niffler::error::Error> {
    let (mut stream, _) = niffler::from_path(file_name)?;

    let mut buf = [0u8; 1];
    match stream.read_exact(&mut buf) {
        Ok(()) => Ok(()),
        Err(_) => Err(niffler::error::Error::FileTooShort),
    };

    let reader = match buf[0] {
        62 => Ok(Reader::FASTQ(fastq::Reader::new(stream))),
        64 => Ok(Reader::FASTA(fasta::Reader::new(stream))),
        _ => Err(niffler::error::Error::IOError),
    };

    Ok(())
}
