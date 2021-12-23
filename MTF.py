# -*- coding: utf-8 -*-
"""
Addapted from:
https://github.com/ArezooAbdollahi/Lossless-image-compression-with-Hilbert-Curve-and-Move-to-Front

"""
import numpy as np


def occurrences_dict(data):
    occurrences = {}

    for i in range(len(data)):
        if data[i] in occurrences:
            occurrences[data[i]] += 1
        else:
            occurrences[data[i]] = 1

    return occurrences


def compress(arr, alphabet):
    # import ipdb; ipdb.set_trace()
    st = list(alphabet)
    #print('Alphabet Data Type: ' + str(alphabet.dtype))
    n = len(arr)
    cw = np.zeros(n, dtype=alphabet.dtype)
    for i in range(n):
        item = arr[i]
        index = st.index(item)
        cw[i] = index
        st.pop(index)
        st = [item] + st
    return cw


def decompress(arr, alphabet):
    st = list(alphabet)
    n = len(arr)
    data = np.zeros(n, dtype=alphabet.dtype)
    # import ipdb; ipdb.set_trace()
    for i in range(n):
        code = arr[i]
        symbol = st[code]
        data[i] = symbol
        st.pop(code)
        st = [symbol] + st
    return data


"""def main():
    filename = 'teste.txt'
    f = open(filename, "rb")
    data = f.read()
    f.close()
    occur = occurrences_dict(data)

    compressed = compress(data, np.array(list(occur.keys())))
    print(compressed)
    f = open('compressed.txt', "wb")
    f.write(compressed.tobytes())
    f.close()

    f = open('compressed.txt', "rb")
    data = f.read()
    f.close()

    data = decompress(data, np.array(list(occur.keys())))
    print(data)

    f = open('bible2.txt', "wb")
    f.write(data.tobytes())
    f.close()

main()"""



