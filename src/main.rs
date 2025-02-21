use std::u8;

fn main() {
    println!("Hello, world!");
    iterate();
}

fn iterate() {
    let mut i: u8 = 1;
    while i < 9 {
        println!("hello");
        i = i + 1;
    }
}
