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
