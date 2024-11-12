![SF archiver](sf_app/gui/img/sf_logo.png)

_Shannon-Fano archiver. <br>
It's an experiment, in which I was making my own archiver with Shannon-Fano algorithm.<br>
After some time I've added Huffman algorithm too._

## Select language

- [English](README.md)
- [Russian](README_ru.md)

## Installation

You can get an executable file for Windows from the [releases](https://github.com/Yarosvet/sf_archiver/releases) page.

Also, you can build it yourself. Just clone the repository:

```bash
git clone https://github.com/Yarosvet/sf_archiver/releases
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

And run the script:

```bash
python main.py
```

Or build it with pyinstaller:

```bash
pip install pyinstaller
pyinstaller --clean sf_archiver.spec
```

## Usage

### CLI

You can use this tool from the command line. Just run the script and follow the instructions.

```
usage: sf_archiver [-h] {compress,decompress,gui} ...

Compress and decompress files using SF Archiver

positional arguments:
  {compress,decompress,gui}
                        Mode of operation
    compress            Compress files
    decompress          Decompress files
    gui                 Run GUI

options:
  -h, --help            show this help message and exit
```

By default, without any arguments, the GUI will be launched.

#### Compress using CLI

```
usage: sf_archiver [-h] {compress,decompress,gui} ...

Compress and decompress files using SF Archiver

positional arguments:
  {compress,decompress,gui}
                        Mode of operation
    compress            Compress files
    decompress          Decompress files
    gui                 Run GUI

options:
  -h, --help            show this help message and exit
```

#### Decompress using CLI

```
usage: sf_archiver decompress [-h] -i INPUT [-o OUTPUT] [-v]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file
  -o OUTPUT, --output OUTPUT
                        Output file or directory (default ./) If no name specified, original name will be used
  -v, --verify          Verify CRC32 checksum stored in compressed file
```

### GUI

Select compression algorithm and press the corresponding button.<br>
It's highly recommended to verify the checksum after decompression.

![GUI](screenshot.png)

## Explore

There is a specification for the format in [sf_kaitai_specification.ksy](sf_kaitai_specification.ksy).<br>
Load it into [Kaitai IDE](https://ide.kaitai.io/) to explore the structure of the compressed file.

## Architecture

The project consists of the following modules:

- `sf_app` - the main package
    - `gui` - Graphical User Interface module (PyQt6)
    - `cli` - CLI module (argparse)
    - `logic` - Module with the main logic of the archiver

All mechanisms are connected by controller in `sf_app/controllers.py`

## Shannon-Fano algorithm

The Shannon-Fano algorithm is a method for constructing a prefix code based on a set of symbols and their
probabilities.<br>
It is used for lossless data compression. The algorithm was independently proposed by Claude Shannon and Robert Fano.

- **Purpose:** To create an efficient binary code for a set of symbols based on their probabilities.

**Process:**

1. Sort the symbols by their probabilities in descending order.
2. Divide the list into two parts, where the total probabilities of both parts are as equal as possible.
3. Assign a binary digit (0 or 1) to each part.
4. Repeat the process recursively for each part until each symbol has a unique binary code.

**Example:**

Given symbols with probabilities:

- A: 0.4
- B: 0.3
- C: 0.2
- D: 0.1

The Shannon-Fano algorithm would generate the following codes:

- A: 0
- B: 10
- C: 110
- D: 111

**Advantages:**

- Simple to implement.
- Provides a prefix code, which means no code is a prefix of another, ensuring unambiguous decoding.

**Disadvantages:**

- May not always produce the most optimal code compared to Huffman coding.

## Huffman algorithm

The Huffman algorithm is a widely used method for lossless data compression. It was developed by David A. Huffman while
he was a Ph.D. student at MIT, and it is used to create an optimal prefix code based on the frequencies of the symbols
in the input data.

- **Purpose:** To create an efficient binary code for a set of symbols based on their frequencies.

**Process:**

- Count the frequency of each symbol in the input data.
- Create a priority queue (min-heap) where each node represents a symbol and its frequency.
- Combine the two nodes with the lowest frequencies to create a new node with a frequency equal to the sum of the two
  nodes' frequencies. This new node becomes the parent of the two nodes.
- Insert the new node back into the priority queue.
- Repeat steps 3 and 4 until there is only one node left in the queue. This node becomes the root of the Huffman tree.
- Assign binary codes to each symbol by traversing the Huffman tree from the root to the leaves. Assign '0' for left
  branches and '1' for right branches.

**Example:**

Given symbols with frequencies:

- A: 5
- B: 9
- C: 12
- D: 13
- E: 16
- F: 45

The Huffman algorithm would generate the following codes:

- F: 0
- C: 100
- D: 101
- A: 1100
- B: 1101
- E: 111

**Advantages:**

- Produces an optimal prefix code, ensuring no code is a prefix of another.
- Efficient for data compression.

**Disadvantages:**

- Requires knowledge of the symbol frequencies beforehand.
- More complex to implement compared to the Shannon-Fano algorithm.