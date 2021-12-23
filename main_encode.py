"""
Trabalho realizado por:
Liu Haolong    nº2018288018
Pedro Oliveira  nº2016255658
Rafael Amaral   nº2018286060
"""

import os
import sys

import numpy as np
from matplotlib import pyplot as plt
import RLE as rle
import BWT as bwt
import huffmancodec as huff
import LZ78 as lz78
import arithmetic_compress as ari1
import adaptive_arithmetic_compress as adap_ari
import ppm_compress as ppm
import SFC as sfc
import LZW as lzw
import MTF as mtf


def occurrences_dict(data):
    occurrences = {}

    for i in range(len(data)):
        if data[i] in occurrences:
            occurrences[data[i]] += 1
        else:
            occurrences[data[i]] = 1

    return occurrences


def load_data(filenames):
    original_files = []
    for i in filenames:
        tmp = []
        f = open(i, "r")
        data = f.read()
        tmp.append(data)
        dicio = occurrences_dict(data)
        tmp.append(dicio)
        original_files.append(tmp)
    return original_files


def viewhistogram(alphabet, occurrences, title):
    plt.figure()
    plt.bar(alphabet, occurrences)
    plt.xlabel("Alphabet Symbols")
    plt.ylabel("Symbol Occurrence")
    plt.title(title)
    plt.tight_layout()
    plt.show()


def entropia(data, occurrences):
    prob = occurrences[occurrences > 0] / len(data)
    return -np.sum(prob * np.log2(prob)), prob


def main():
    filenames = ['bible.txt', 'finance.csv', 'jquery-3.6.0.js', 'random.txt']
    original_files = load_data(filenames)
    flags = [False] * len(filenames)
    for i in range(len(original_files)):
        sorted_keys = sorted(original_files[i][1].keys())
        sorted_dict = {key: original_files[i][1][key] for key in sorted_keys}
        # print(sorted_dict)
        # viewhistogram(list(sorted_dict.keys()), list(sorted_dict.values()), filenames[i])
        entropy, prob = entropia(original_files[i][0], np.array(list(original_files[i][1].values())))
        print(filenames[i] + ' File Size {} Bytes (without compression)'.format(os.path.getsize(filenames[i])))
        print(filenames[i] + ' Entropy = {} bits/symbol'.format(entropy))
        for opcao in sys.argv[1:]:
            if opcao == '-rle':
                # Run Length Encoding
                print("rle")
                f = open(filenames[i] , "rb")
                data = f.read()
                f.close()
                #print("xd: " + filenames[i][-2:])
                if filenames[i][-2:] == 'js':
                    #print("here")
                    filenames[i] = filenames[i][:-3] + '.rle.txt'
                else:
                    filenames[i] = filenames[i][:-4] + '.rle.txt'
                #print(filenames[i])
                #f1 = open(filenames[i], "x")
                #f1.close()
                f1 = open(filenames[i], "wb")
                compressed_data = rle.compress(data)
                f1.write(compressed_data.tobytes())
                f1.close()
                flags[i] = True
            if opcao == '-bwt':
                # Burrows Wheeler Transform
                print("bwt")
                f = open(filenames[i], "rb")
                data = f.read()
                f.close()
                if filenames[i][-2:] == 'js':
                    # print("here")
                    filenames[i] = filenames[i][:-3] + '.bwt.txt'
                else:
                    filenames[i] = filenames[i][:-4] + '.bwt.txt'
                f1 = open(filenames[i], "wb")
                bwt_ref, idx = bwt.bwt(data)
                encoded = [data[x] for x in bwt_ref]
                if idx < 2 ** 8 or idx >= 0:
                    tp = np.uint8
                elif idx < 2 ** 8 / 2 or idx >= -2 ** 8 / 2:
                    tp = np.int8
                elif idx < 2 ** 16 or idx >= 0:
                    tp = np.uint16
                elif idx < 2 ** 16 / 2 or idx >= -2 ** 16 / 2:
                    tp = np.int16
                elif idx < 2 ** 32 or idx >= 0:
                    tp = np.uint32
                elif idx < 2 ** 32 / 2 or idx >= -2 ** 32 / 2:
                    tp = np.int32
                data_comp = np.append(np.array(encoded), [idx]).astype(tp)
                f1.write(data_comp.tobytes())
                f1.close()
                flags[i] = True
            if opcao == '-huff':
                # Huffman
                print("huff")
                f = open(filenames[i], "rb")
                data = f.read()
                f.close()
                if filenames[i][-2:] == 'js':
                    # print("here")
                    filenames[i] = filenames[i][:-3] + '.huff.txt'
                else:
                    filenames[i] = filenames[i][:-4] + '.huff.txt'
                f1 = open(filenames[i], "wb")
                codec = huff.HuffmanCodec.from_data(data)
                f1.write(codec.encode(data))
                f1.close()
                flags[i] = True
            if opcao == '-lz78':
                # LZ78
                print("lz78")
                inputFile = filenames[i]
                if filenames[i][-2:] == 'js':
                    # print("here")
                    filenames[i] = filenames[i][:-3] + '.lz78.txt'
                else:
                    filenames[i] = filenames[i][:-4] + '.lz78.txt'
                lz78.lz78_compress(inputFile, filenames[i])
                flags[i] = True
            if opcao == '-ari':
                # Arithmetic
                print("ari")
                inputFile = filenames[i]
                if filenames[i][-2:] == 'js':
                    # print("here")
                    filenames[i] = filenames[i][:-3] + '.ari.txt'
                else:
                    filenames[i] = filenames[i][:-4] + '.ari.txt'
                ari1.ari(inputFile, filenames[i])
                flags[i] = True
            if opcao == '-adapt_ari':
                # Adaptive Arithmetic
                print("adapt ari")
                inputFile = filenames[i]
                if filenames[i][-2:] == 'js':
                    # print("here")
                    filenames[i] = filenames[i][:-3] + '.adapt_ari.txt'
                else:
                    filenames[i] = filenames[i][:-4] + '.adapt_ari.txt'
                adap_ari.ari(inputFile, filenames[i])
                flags[i] = True
            if opcao == '-ppm':
                # Prediction by Partial Matching
                print("ppm")
                inputFile = filenames[i]
                if filenames[i][-2:] == 'js':
                    # print("here")
                    filenames[i] = filenames[i][:-3] + '.ppm.txt'
                else:
                    filenames[i] = filenames[i][:-4] + '.ppm.txt'
                ppm.ppm(inputFile, filenames[i])
                flags[i] = True
            if opcao == '-sfc': #not working
                # Shannon Fano Coding
                print("sfc")
                inputFile = filenames[i]
                if filenames[i][-2:] == 'js':
                    # print("here")
                    filenames[i] = filenames[i][:-3] + '.sfc.txt'
                else:
                    filenames[i] = filenames[i][:-4] + '.sfc.txt'
                sfc.sfc(inputFile, filenames[i], 'e')
                flags[i] = True
            if opcao == '-lzw':
                # LZW
                print("lzw")
                inputFile = filenames[i]
                data = lzw.readbytes(inputFile)
                if filenames[i][-2:] == 'js':
                    # print("here")
                    filenames[i] = filenames[i][:-3] + '.lzw.txt'
                else:
                    filenames[i] = filenames[i][:-4] + '.lzw.txt'
                lzw.writebytes(filenames[i], lzw.compress(data))
                flags[i] = True
            if opcao == '-mtf': #not working
                # Move To Front
                print("mtf")
                f = open(filenames[i], "rb")
                data = f.read()
                f.close()
                occur = occurrences_dict(data)

                compressed_data_array = mtf.compress(data, np.array(list(occur.keys())))

                if filenames[i][-2:] == 'js':
                    # print("here")
                    filenames[i] = filenames[i][:-3] + '.mtf.txt'
                else:
                    filenames[i] = filenames[i][:-4] + '.mtf.txt'
                f1 = open(filenames[i], "wb")
                f1.write(compressed_data_array.tobytes())
                f1.close()
                flags[i] = True


main()
