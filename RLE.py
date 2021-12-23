"""Run Length Encoding utilities for NumPy arrays.
Authors
-------
- Nezar Abdennur
- Anton Goloborodko
"""
from __future__ import division, print_function
import numpy as np
import math
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain, groupby
from collections import Counter
import operator

import numpy as np

# Python code for run length encoding
from collections import OrderedDict

"""def runLengthDecoding(compressed_seq):
    seq = ''
    for i in range(0, len(compressed_seq)):
        if compressed_seq[i].isnumeric() == False:
            for j in range(int(compressed_seq[i + 1])):
                seq += compressed_seq[i]

    return (seq)"""


def convertascii(data):
    newasciidata = np.zeros(len(data))
    j = 0
    for i in data:
        newasciidata[j] = ord(i)
        j += 1
    return newasciidata


def reverseascii(data):
    new_data = ''
    for i in data:
        new_data += chr(i)
    return new_data


def runLengthDecoding(compressed_seq):
    seq = ''
    i = 0
    # print("xd" + compressed_seq[58782] + "xd1" + compressed_seq[58783] + "xd2")
    while i < len(compressed_seq):
        # print(i)
        for j in range(int(compressed_seq[i + 1])):
            seq += str(compressed_seq[i])
        i += 2
    return seq


def runLengthEncoding(seq):
    compressed = []
    count = 1
    char = seq[0]
    for i in range(1, len(seq)):
        if seq[i] == char:
            count = count + 1
        else:
            compressed.append([char, count])
            char = seq[i]
            count = 1
    compressed.append([char, count])
    # print(compressed)
    return compressed


def viewhistogram(alphabet, occurrences, title):
    array = []
    if title == "data/english.txt":
        i = 0
        for i in range(len(alphabet)):
            array.append(chr(alphabet[i]))
        alphabet = array

    plt.figure()
    plt.bar(alphabet, occurrences)
    plt.xlabel("Alphabet Symbols")
    plt.ylabel("Symbol Occurrence")
    plt.title(title)
    plt.tight_layout()
    plt.show()


def occurrences_dict(data):
    occurrences = {}

    for i in range(len(data)):
        if data[i] in occurrences:
            occurrences[data[i]] += 1
        else:
            occurrences[data[i]] = 1

    return occurrences


def rle(data):
    compressed = runLengthEncoding(data)
    compressed_seq = ''

    for k in range(0, len(compressed)):

        for j in compressed[k]:
            compressed_seq += str(j)
    return compressed_seq


def compress(iterable):
    # iterable = convertascii(data)
    compList = list(chain.from_iterable(
        (val, len([*thing]))
        for val, thing in groupby(iterable)
    ))
    ma = max(compList)
    mi = min(compList)
    if ma < 2 ** 8 and mi >= 0:
        return np.array(compList, dtype=np.uint8)
    elif ma < 2 ** 8 / 2 and mi >= -2 ** 8 / 2:
        return np.array(compList, dtype=np.int8)
    elif ma < 2 ** 16 and mi >= 0:
        return np.array(compList, dtype=np.uint16)
    elif ma < 2 ** 16 / 2 and mi >= -2 ** 16 / 2:
        return np.array(compList, dtype=np.int16)
    elif ma < 2 ** 32 and mi >= 0:
        return np.array(compList, dtype=np.uint32)
    elif ma < 2 ** 32 / 2 and mi >= -2 ** 32 / 2:
        return np.array(compList, dtype=np.int32)
    else:
        return np.array(compList)





def decompress(data):
    d = np.frombuffer(data, dtype=np.uint8)
    vals = d[::2]
    # print(vals)
    reps = d[1::2]
    # print(reps)
    # for j in reps:
    # print(reps)
    decompressed = np.array([])
    for i in range(len(vals)):
        aux = np.empty(reps[i])
        aux[:] = vals[i]
        decompressed = np.append(decompressed, aux)
    # print(len(decompressed))
    return decompressed.astype(np.uint8)


"""def main():
    filenames = ['bible.txt', 'finance.csv', 'jquery-3.6.0.js', 'random.txt']

    f = open('teste.txt', "rb")
    data = f.read()
    f.close()
    compressed_seq = compress(data)
    comp = ''
    for i in compressed_seq:
        comp += str(i)
    f = open('compressed.txt', "wb")
    f.write(compressed_seq.tobytes())
    f.close()

    f = open('compressed.txt', "rb")
    data = f.read()
    decompressed = decompress(data)
    f.close()

    f = open('bible2.txt', "wb")
    f.write(decompressed)
    f.close



main()"""
