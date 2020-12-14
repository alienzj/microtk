use std::io;
use bio::io::fastq;
use bio::io::fastq::FastqRead;

fn main() {
    let mut reader = fastq::Reader::new(io::stdin());

    let mut nb_reads = 0;
    let mut nb_bases = 0;

    for result in reader.records() {
        let record = result.expect("Error during fastq record parsing");

        nb_reads += 1;
        nb_bases += record.seq().len();
    }

    println!("Number of reads: {}", nb_reads);
    println!("Number of reads: {}", nb_bases);
}
