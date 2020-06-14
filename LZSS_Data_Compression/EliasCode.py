# Chia Wei Ying
# 30113199
from bitarray import bitarray

class EliasCode:
    # Input: bitarray() of an int
    #     Convert this bitarray() of int to elias code
    #     call .getEliasCode() to get the elias code of the input bitstring
    def __init__(self, _bin):
        self.elias = _bin # actual elias code to be returned, bin is preloaded into it
        self.encodeElias(len(_bin))  # start encoding

    "Function that convert decimal to elias code"
    # Input:  int to be converted to elias needed bitstring format
    # Return: elias needed bitstring format in proper format
    def getEliasBinary(self, dec):
        x = bitarray(format(dec, 'b'))
        x[0] = False    # convert the most significant bit to 0
        return x

    "Recursively encode bin"
    # Input: length of the previous binary encoded
    # 
    #     Base case when length of the binary to be encoded is 1
    def encodeElias(self, l):
        if l != 1:
            l -= 1
            encodedLen = self.getEliasBinary(l)
            self.elias = encodedLen + self.elias
            self.encodeElias(len(encodedLen))
            if l == 1:  # base case
                return True

    "An API function to get the encoded elias of _bin"
    # Return: the encoded elias of self.bin in bitstring
    def getEliasCode(self):
        return self.elias