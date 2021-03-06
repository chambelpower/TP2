# 
# Compression application using adaptive arithmetic coding
# 
# Usage: python adaptive-arithmetic_compress.py InputFile OutputFile
# Then use the corresponding adaptive-arithmetic_decompress.py application to recreate the original input file.
# Note that the application starts with a flat frequency table of 257 symbols (all set to a frequency of 1),
# and updates it after each byte encoded. The corresponding decompressor program also starts with a flat
# frequency table and updates it after each byte decoded. It is by design that the compressor and
# decompressor have synchronized states, so that the data can be decompressed properly.
# 
# Copyright (c) Project Nayuki
# 
# https://www.nayuki.io/page/reference-arithmetic-coding
# https://github.com/nayuki/Reference-arithmetic-coding
# 

import contextlib, sys
import arithmeticcoding


def ari(inputFile, outputFile):
    # Perform file compression
    with open(inputFile, "rb") as inp, \
            contextlib.closing(arithmeticcoding.BitOutputStream(open(outputFile, "wb"))) as bitout:
        compress(inp, bitout)

"""
# Command line main application function.
def main(args):
    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: python adaptive-arithmetic_compress.py InputFile OutputFile")
    inputfile, outputfile = args

    # Perform file compression
    with open(inputfile, "rb") as inp, \
            contextlib.closing(arithmeticcoding.BitOutputStream(open(outputfile, "wb"))) as bitout:
        compress(inp, bitout)
"""

def compress(inp, bitout):
    initfreqs = arithmeticcoding.FlatFrequencyTable(257)
    freqs = arithmeticcoding.SimpleFrequencyTable(initfreqs)
    enc = arithmeticcoding.ArithmeticEncoder(32, bitout)
    while True:
        # Read and encode one byte
        symbol = inp.read(1)
        if len(symbol) == 0:
            break
        enc.write(freqs, symbol[0])
        freqs.increment(symbol[0])
    enc.write(freqs, 256)  # EOF
    enc.finish()  # Flush remaining code bits


