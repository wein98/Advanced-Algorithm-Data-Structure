# Chia Wei Ying
# 30113199

import sys
from FibonacciHeap import *
from common import *
from EliasCode import *

class LZSS_encoder:
    def __init__(self, txt, w, l):
        self.txt = txt
        self.window = w
        self.buffer = l
        self.length = len(txt)
        self.uniqueChar = []    # ["ASCII char", "char freq", "huffman code word", "length of huffman"]
        # set up an amap for easy assess of unique chars in self.txt
        self.amap = [None for _ in range(128)]
        self.getAmap()
        # get the total number of unique characters in self.txt in elias code format
        self.uniqueCharLenElias = EliasCode(getBinary(len(self.uniqueChar))).getEliasCode()
        # compute huffman word core for each unique characters populated to self.uniqueChar
        self.huffmanWordCode()
        # compute the header part
        self.header = self.computeHeader()
        # compute the data part
        self.data = self.computeData()
        # output to file
        self.output()

    "Function that set up an amap for easy assess of unique chars in self.txt and also computes"
    "the frequency of each unique chars"
    # O(n+m) - n is length self.txt, m is total number of unique chars in self.txt
    def getAmap(self):
        count = 0
        for i in range(self.length):
            k = getOrd(self.txt[i])
            if self.amap[k] == None:
                self.amap[k] = count
                self.uniqueChar.append([self.txt[i], 1])
                count += 1
            else:
                self.uniqueChar[self.amap[k]][1] += 1

        # compute frequency for self.uniqueChar
        n = len(self.uniqueChar)
        for i in range(n):
            self.uniqueChar[i][1] = round(self.uniqueChar[i][1]/n, 2)

    "Function that computes huffman wordcode for each unique characters in self.uniquechar"
    # O(m) - m is total number of unique chars in self.txt
    def huffmanWordCode(self):
        # insert all unique characters to fibonacci heap
        heap = FibonacciHeap()

        for i in range(len(self.uniqueChar)):
            self.uniqueChar[i].append("")   # to store huffman wordcode
            heap.insert(self.uniqueChar[i][1], self.uniqueChar[i][0])

        # start building huffman word for each unique chars from the heap
        if len(self.uniqueChar) > 1:
            while heap.size > 0:
                x = heap.extractMin()
                y = heap.extractMin()

                for i in range(len(x.payload)):
                    self.uniqueChar[self.amap[getOrd(x.payload[i])]][2] += "0" 
                    
                for i in range(len(y.payload)):
                    self.uniqueChar[self.amap[getOrd(y.payload[i])]][2] += "1"

                resultKey = x.key + y.key
                resultPayload = x.payload + y.payload

                if heap.size > 0:
                    heap.insert(resultKey, resultPayload)
        else:   # handles condition when there is only one unique character
            x = heap.extractMin()
            self.uniqueChar[self.amap[getOrd(x.payload[i])]][2] += "0" 

        # flip the huffman wordcode for each unique characters
        for i in range(len(self.uniqueChar)):
            flip = self.uniqueChar[i][2][::-1]

            # compute elias code of length of huffman codeword for each uniqueChar
            eliasLen = EliasCode(getBinary(len(flip))).getEliasCode()
            self.uniqueChar[i][2] = flip
            self.uniqueChar[i].append(eliasLen)

    "Function that encodes the header part with all the precomputed variables"
    # Return:   encoded LZSS for the header part
    # O(m) - m is total number of unique chars in self.txt
    def computeHeader(self):
        retVal = self.uniqueCharLenElias

        for i in range(len(self.uniqueChar)):
            x = self.uniqueChar[i]
            retVal += ASCIItoBin(x[0])
            retVal += x[3]  # huffman codeword length
            retVal += x[2]  # huffman codeword

        return retVal

    "Function that compute LZSS format for each buffered window"
    # Due to slicing used, I'm not very sure about the big-O, however the big-O here is just sucks!
    def ZAlgo(self, k):
        x = k - self.window
        window = self.window
        buffer = self.buffer

        # tweak the window size if len of string[0:k] < self.window
        if x < 0:
            x = 0
            window = k-x

        # tweak the buffer size if len of string[k:self.length] < self.buffer
        if self.buffer + k >= self.length:
            buffer = self.length-k
        
        slicing = self.txt[k:k+buffer] + "$" + self.txt[x:k+buffer]
        
        z = zAlgo(slicing)
        length = 0
        offset = 0
        for i in range(self.buffer, buffer+window+1):
            if z[i] > length: # get the max length
                length = z[i]
                offset = window-(i-buffer-1)
            elif z[i] == length:  # get the offset index when there is same max before
                offset = window-(i-buffer-1)

        return offset, length

    "Function that gets the LZSS Format-0/1 fields"
    # Return: the LZSS Format-0/1 fields
    def computeLZSS(self):
        j = 2   # j always starts from 2, since len < 3 always uses 1-bit in LZSS
        retVal = [[1, self.txt[0]], [1, self.txt[1]]]
        while j < self.length:
            offset, length = self.ZAlgo(j) 
            # LZSS rule, length >= 3
            if length >= 3:
                retVal.append([0, offset, length])
                length -= 1
            else:
                retVal.append([1, self.txt[j]])
                length = 0
            j += length+1

        return retVal

    "Function that retunrs the encoded data part"
    # Return: the encoded data part
    def computeData(self):
        lzssFormat = self.computeLZSS()
        data = EliasCode(getBinary(len(lzssFormat))).getEliasCode()
        
        for i in range (len(lzssFormat)):
            if lzssFormat[i][0] == 1:
                data += "1" + self.uniqueChar[self.amap[getOrd(lzssFormat[i][1])]][2]   
            else:
                data += "0" + EliasCode(getBinary(lzssFormat[i][1])).getEliasCode() + EliasCode(getBinary(lzssFormat[i][2])).getEliasCode()
        
        return data

    "Function that outputs the entired encoded bitstring of the compression of self.txt"
    def output(self):
        data = self.header + self.data
        print(data)
        x = len(data) % 8
        # do padding of 0s to the end of the encoded string if len(data) is not a factor of 8
        if x != 0:
            pad = '0'*(8-x)
            data += pad
        
        print(data)

        byteArray = bytearray()
        chop = [data[i : i + 8] for i in range(0, len(data), 8)]
        for i in range(len(chop)):
            byteArray.append(int(chop[i], 2))

        file = open('output_encoder_lzss.bin', "wb")
        file.write(byteArray)
        file.close()

if __name__ == "__main__":
    # >>python encoder_lzss.py  <input_text_file> <W> <L>
    txtF = open(sys.argv[1], "r")
    w = sys.argv[2]
    l = sys.argv[3]

    for line in txtF:
        LZSS_encoder(line, int(w), int(l))