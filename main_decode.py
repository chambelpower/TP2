"""
Trabalho realizado por:
Liu Haolong    nº2018288018
Pedro Oliveira  nº2016255658
Rafael Amaral   nº2018286060
"""
import os
import stat
import sys


import numpy as np
from matplotlib import pyplot as plt
import RLE as rle
import BWT as bwt
import huffmancodec as huff
import LZ78 as lz78
import arithmetic_decompress as ari_decomp
import adaptive_arithmetic_decompress as adap_ari_decomp
import ppm_decompress as ppm_decomp
import SFC as sfc
import LZW as lzw
import MTF as mtf


def decompress(compressedFile):
    decompressionOps = ['rle', 'bwt', 'huff', 'lz78', 'ari', 'adapt_ari', 'ppm', 'sfc', 'lzw', 'mtf']
    splitted = compressedFile.split('.')
    if splitted[0] == 'jquery-3':
        t = splitted[3:]
        splitted = []
        splitted.append('jquery-3.6.0')
        for k in t:
            splitted.append(k)
        #print(splitted)
    if len(splitted) <= 1:
        print("Error: file is not compressed")
        return
    outName = ''
    for compOp in splitted[1:-1]:
        if compOp not in decompressionOps:
            print('This descompressor does not support' + compOp.upper() + ' compression')
            return
        outName += '_' + compOp
    fi = open(compressedFile, "rb")
    data = fi.read()
    fi.close()

    f1 = open('tmp.txt', "wb")
    f1.write(data)
    f1.close()
    for i in range(len(splitted) - 2, 0, -1):
        print(splitted[i])
        if splitted[i] == 'rle':
            print("here")
            f1 = open("tmp.txt", "rb")
            data = f1.read()
            f1.close()
            data = rle.decompress(data)
            f1 = open("tmp.txt", "wb")
            f1.write(data)
            f1.close()

        elif splitted[i] == 'bwt':
            f1 = open("tmp.txt", "rb")
            data = f1.read()
            f1.close()
            ibwt_ref = bwt.ibwt(data[:-1], data[-1])
            decoded = [data[x] for x in ibwt_ref]
            decoded = np.array(decoded)
            decoded = np.array(decoded)
            str = ''
            for k in decoded:
                str += chr(k)

            f1 = open("tmp.txt", "wb")
            f1.write(bytes(str, 'utf-8'))
            f1.close()

        elif splitted[i] == 'huff':
            f1 = open("tmp.txt", "rb")
            data = f1.read()
            f1.close()
            data = huff.PrefixCodec.decode(data)
            f1 = open("tmp.txt", "wb")
            f1.write(data)
            f1.close()

        elif splitted[i] == 'lz78':
            lz78_d = lz78.LZ78Decompressor('tmp.txt')
            lz78_d.decompress('tmp.txt', 'tmp.txt')

        elif splitted[i] == 'ari':
            ari_decomp.decompress_ari('tmp.txt', 'tmp.txt')

        elif splitted[i] == 'adapt_ari':
            adap_ari_decomp.adap_decomp('tmp.txt', 'tmp.txt')

        elif splitted[i] == 'ppm':
            ppm_decomp.ppm_decomp('tmp.txt', 'tmp.txt')

        elif splitted[i] == 'sfc':
            sfc.sfc('tmp.txt', 'tmp.txt', 'd')  # not working?

        elif splitted[i] == 'lzw':
            f1 = open("tmp.txt", "rb")
            data = f1.read()
            f1.close()
            data = lzw.decompress(data)
            f1 = open("tmp.txt", "wb")
            f1.write(data)
            f1.close()

        elif splitted[i] == 'mtf': #not working
            f1 = open("tmp.txt", "rb")
            data = f1.read()
            f1.close()
            data = mtf.decompress(data, np.arange())#alfabeto?
            f1 = open("tmp.txt", "wb")
            f1.write(data)
            f1.close()

    f1 = open(splitted[0] + 'decompressed.txt', "wb")
    f2 = open('tmp.txt', "rb")
    data = f2.read()
    f1.write(data)
    f1.close()
    f2.close()


def main():
    filenames = os.listdir()

    final_file_list = []
    current_bible_file = 'bible.txt'
    current_financial_file = 'finance.csv'
    current_java_file = 'jquery-3.6.0.js'
    current_random_file = 'random.txt'
    for file in filenames:
        #print(file)
        var = file.split('.')
        if var[0] == 'bible':
            #print(len(file))
            #print(len(current_bible_file))
            if len(file) > len(current_bible_file):
                current_bible_file = file
        elif var[0] == 'finance':
            if len(file) > len(current_financial_file):
                current_financial_file = file
        elif var[0] == 'jquery-3':
            if len(file) > len(current_java_file):
                current_java_file = file
        elif var[0] == 'random':
            if len(file) > len(current_random_file):
                current_random_file = file

    final_file_list.append(current_bible_file)
    final_file_list.append(current_financial_file)
    final_file_list.append(current_java_file)
    final_file_list.append(current_random_file)
    print(final_file_list)
    for file in final_file_list:
        decompress(file)

    for file in filenames:
        var = file.split('.')
        if var[0] == 'bible' and file != 'bible.txt':
            os.remove(file)
        if var[0] == 'finance' and file != 'finance.csv':
            os.remove(file)
        if var[0] == 'jquery-3' and file != 'jquery-3.6.0.js':
            os.remove(file)
        if var[0] == 'random' and file != 'random.txt':
            os.remove(file)


if __name__ == "__main__":
    main()
