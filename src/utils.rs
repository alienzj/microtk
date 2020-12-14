// https://github.com/natir/fpa/blob/master/src/file.rs
use std::io;
use std::io::{BufReader, BufWriter};

pub fn get_input(input_name: &str) -> (Box<dyn io::Read>, niffler::compression::Format) {
    match input_name {
        "-" => niffler::get_reader(Box::new(BufReader::new(io::stdin())))
            .expect("File is probably empty"),
        _ => niffler::from_path(input_name).expect("File is probably empty"),
    }
}

pub fn choose_compression(
    input_compression: niffler::compression::Format,
    compression_set: bool,
    compression_value: &str,
) -> niffler::compression::Format {
    if !compression_set {
        return input_compression;
    }
    match compression_value {
        "gzip" => niffler::compression::Format::Gzip,
        "bzip2" => niffler::compression::Format::Bzip,
        "lzma" => niffler::compression::Format::Lzma,
        _ => niffler::compression::Format::No,
    }
}

pub fn get_output(output_name: &str, format: niffler::compression::Format) -> Box<dyn io::Write> {
    match output_name {
        "-" => niffler::get_writer(
            Box::new(BufWriter::new(io::stdout())),
            format,
            niffler::compression::Level::One,
        )
        .unwrap(),
        _ => niffler::to_path(output_name, format, niffler::compression::Level::One).unwrap(),
    }
}

// reference
// https://github.com/ekimb/rust-mdbg/blob/master/src/utils.rs

pub fn revcomp(dna: &str) -> String {
    dna.chars()
        .rev()
        .map(|a| switch_base(a))
        .collect::<String>()
}

fn switch_base(c: char) {
    match c {
        'a' => 't',
        'c' => 'g',
        't' => 'a',
        'g' => 'c',
        'u' => 'a',
        'A' => 'T',
        'C' => 'G',
        'T' => 'A',
        'G' => 'C',
        'U' => 'A',
        _ => 'N',
    }
}
