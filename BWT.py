import math
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain, groupby
from collections import Counter
import operator
import numpy as np

#
# Burrows Wheeler Transform implemented in Python
# Currently, list.sort() is not the radix sort, so the algorithm order is O(n log n log n).
# This algorithm replaces items of arr to integers, so we can use the radix sort instead.
# In that case, the algorithm order becomes O(n log n).
#

from operator import itemgetter

argsort = lambda l: [i for i, _ in sorted(enumerate(l), key=itemgetter(1))]


def suffix_array(arr):
    arr_size = len(arr)
    arr_int = {v: k for k, v in enumerate(sorted(set(arr)))}
    arr = [arr_int[x] for x in arr]
    arr.append(-1)
    suf = [[i, arr[i], arr[i + 1]] for i in range(arr_size)]
    suf.sort(key=itemgetter(1, 2))
    idx = [0] * arr_size
    k = 2
    while k < arr_size:
        r = 0
        prev_r = suf[0][1]
        for i in range(arr_size):
            if suf[i][1] != prev_r or suf[i - 1][2] != suf[i][2]:
                r += 1
            prev_r = suf[i][1]
            suf[i][1] = r
            idx[suf[i][0]] = i
        for i in range(arr_size):
            next_idx = suf[i][0] + k
            suf[i][2] = suf[idx[next_idx]][1] if next_idx < arr_size else -1
        suf.sort(key=itemgetter(1, 2))
        k <<= 1
    return [x[0] for x in suf]


def bwt(data):
    data_ref = suffix_array(data)
    return (x - 1 for x in data_ref), data_ref.index(0)


def ibwt(data, idx):
    sorted_data_ref = argsort(data)
    for i in range(len(data)):
        idx = sorted_data_ref[idx]
        yield idx


def bwt1(data):
    bwt_ref, idx = bwt(data)
    compressed = [data[x] for x in bwt_ref]
    compressed_seq = ''
    for k in range(0, len(compressed)):
        compressed_seq += compressed[k]
    return compressed_seq


"""def main():
    f = open('teste.txt', 'rb')

    data = f.read()
    f.close()

    bwt_ref, idx = bwt(data)
    encoded = [data[x] for x in bwt_ref]
    if (idx < 2 ** 8 or idx >= 0):
        tp = (np.uint8)
    elif (idx < 2 ** 8 / 2 or idx >= -2 ** 8 / 2):
        tp = (np.int8)
    elif (idx < 2 ** 16 or idx >= 0):
        tp = (np.uint16)
    elif (idx < 2 ** 16 / 2 or idx >= -2 ** 16 / 2):
        tp = (np.int16)
    elif (idx < 2 ** 32 or idx >= 0):
        tp = (np.uint32)
    elif (idx < 2 ** 32 / 2 or idx >= -2 ** 32 / 2):
        tp = (np.int32)
    data_comp = np.append(np.array(encoded),[idx]).astype(tp)
    f = open('compressed.txt', "wb")
    f.write(data_comp.tobytes())
    f.close()

    f = open('compressed.txt', "rb")
    data = f.read()
    ibwt_ref = ibwt(data[:-1],data[-1])
    decoded = [data[x] for x in ibwt_ref]
    print(decoded)

    f = open('bible2.txt', "wb")
    decoded = np.array(decoded)
    str = ''
    for k in decoded:
        str+=chr(k)
    f.write(bytes(str, 'utf-8'))
    f.close()



main()"""


