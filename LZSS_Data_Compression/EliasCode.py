# Chia Wei Ying
# 30113199

class EliasCode:
    # Input: bitstring of an int
    #     Convert this bitstring of int to elias code
    #     call .getEliasCode() to get the elias code of the input bitstring
    def __init__(self, bin):
        self.bin = bin  # int that is already converted to bitstring and to be encoded in elias code  
        self.elias = [bin]  # actual elias code to be returned, bin is preloaded into it
        self.encodeElias(len(bin))  # start encoding

    "Function that convert decimal to bitstring format that is needed for elias encoding"
    # Input:  int to be converted to elias needed bitstring format
    # Return: elias needed bitstring format in inversed format
    def EliasBitStringConversion(self, dec):
            if dec == 1:
                return "0"
            if dec % 2 == 0:
                return "0" + self.EliasBitStringConversion(dec//2)
            else:
                return "1" + self.EliasBitStringConversion(dec//2)

    "Function that convert decimal to elias code"
    # Input:  int to be converted to elias needed bitstring format
    # Return: elias needed bitstring format in proper format
    def getEliasBinary(self, dec):
        return self.EliasBitStringConversion(dec)[::-1]

    "Recursively encode self.bin"
    # Input: length of the previous binary encoded
    # 
    #     Base case when length of the binary to be encoded is 1
    def encodeElias(self, l):
        if l != 1:
            l -= 1
            encodedLen = self.getEliasBinary(l)
            self.elias.append(encodedLen)
            self.encodeElias(len(encodedLen))
            if l == 1:
                return True

    "An API function to get the encoded elias of self.bin"
    # Return: the encoded elias of self.bin in bitstring
    def getEliasCode(self):
        retVal = ""
        for i in range(len(self.elias)-1, -1, -1):
            retVal += self.elias[i]

        return retVal