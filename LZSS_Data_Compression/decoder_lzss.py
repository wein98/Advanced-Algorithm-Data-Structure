# Chia Wei Ying
# 30113199

import sys
from HuffmanTree import *

class decoder_lzss:
    def __init__(self, _filename):
        # read input .bin file and convert it to bitstring
        self.bitString = self.processBinFile(_filename)
        self.pointer = 0    # pointer to know up to where the bitstring has been decoded
        # get the length of the unique chars 
        self.uniqueCharLen = self.decodeElias()
        # build a huffman tree for decoding process
        self.huffmanTree = HuffmanTree()
        # decode the header part
        self.decodeHeader()
        # decode the data part
        self.data = self.decodeData()
        self.output()


    "Function that converts .bin file to bitstring to be used in the algorithm"
    def processBinFile(self, filename):
        lol = open(filename, "rb")
        retVal = ""

        byte = lol.read(1)

        while byte:
            x = int.from_bytes(byte, byteorder='big')
            retVal += '{0:08b}'.format(x)
            byte = lol.read(1)

        return retVal

    "Function that mainly decode all the encoded elias portions of the bitstring"
    # Return:   the int of the encoded elias
    # automatically updates the pointer after decoded a portion of elias
    def decodeElias(self):
        temp = ''
        elias = True
        
        if self.bitString[self.pointer] == '0':
            temp = '1'
            self.pointer += 1
        else:   # if elias code starts with 1, return 1
            self.pointer += 1
            return 1

        while(True):
            decodeLen = int(temp, 2) + 1    # length of next chunk to decode
            temp = ''

            for i in range(decodeLen):
                # integer found, not elias code anymore
                if i == 0 and self.bitString[self.pointer] == '1':
                    elias = False
                elif i == 0 and self.bitString[self.pointer] == '0':
                    temp += '1'
                    continue

                temp += self.bitString[self.pointer+i]

            self.pointer += decodeLen 

            if not elias:   # return integer
                return int(temp, 2)   

    "Function that decodes the header part"
    # main purpose is to decode the huffman codeword of each unique char that is from elias
    # and populate them to self.huffmantree
    def decodeHeader(self):
        temp = ''

        for _ in range(self.uniqueCharLen):
            temp = self.bitString[self.pointer:self.pointer+7]  # get ASCII 7 bits
            self.pointer += 7   # shift pointer
            char = chr(int(temp, 2))    # convert 7-bits to ASCII char
            huffmanLen = self.decodeElias() # get huffman codeword length for this char
            huffmanCode = self.bitString[self.pointer: self.pointer+huffmanLen] # get huffman codeword for this char
            self.huffmanTree.insertNode(char, huffmanCode)    # insert to huffmanTree for retrieval when decoding data part
            # self.uniqueChar.append([char, huffmanCode]) # store ASCII char and its huffman code
            self.pointer += huffmanLen  # shift pointer

        # print(self.uniqueChar)

    "Function that decodes the data part"
    # Return:   the decoded data
    def decodeData(self):
        # get total number of elias Format fields
        formatNo = self.decodeElias()
        data = ''

        for _ in range(formatNo):
            if self.bitString[self.pointer] == '1':  # Format 1
                self.pointer += 1
                node = self.huffmanTree.root

                # traverse through the huffman tree until a leaf is found, then get the unique char
                while (True):
                    node = self.huffmanTree.getNode(node, self.bitString[self.pointer])
                    self.pointer += 1
                    if node.leaf:   # found char
                        data += node.char   # add char to data
                        break
            else:   # Format 0
                self.pointer += 1
                offset = self.decodeElias()
                length = self.decodeElias()
                start = len(data)-offset

                for j in range(length):
                    data += data[start+j]

        print(data)
        return data
            
    "Function that output the decoded data to a file"
    def output(self):
        file = open("output_decoder_lzss.txt", "w+")
        file.write(self.data)
        file.close()
                    
if __name__ == "__main__":
    # >>python decoder_lzss.py <output_encoder_lzss.bin>
    decoder_lzss(sys.argv[1])