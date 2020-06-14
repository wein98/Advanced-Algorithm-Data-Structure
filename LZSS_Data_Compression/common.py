# Chia Wei Ying
# 30113199
from bitarray import bitarray

# convert ASCII char to bitarray
def ASCIItoBin(char):
    x = format(getOrd(char), 'b')
    if len(x) < 7:
        pad = '0'*(7-len(x))
        x = pad + x
    return bitarray(x)

# get ASCII value in dec
def getOrd(x):
    return ord(x)

# get bitarray of dec
# O(log n) - n = dec
def getBinary(dec):
    return bitarray(format(dec, 'b'))

# get decimal from bitarray
# O(n) - n is length of bits in bitarray
def getDecFromBin(b):
    i = 0
    for bit in b:
        i = (i << 1) | bit

    return i

# Gusfield's Z-algorithm
# O(n) - n is len(string)
def zAlgo(string):
    n = len(string)
    zArr = [0]*n
    zArr[0] = n     # set first zArr to length of string
    L = 0
    R = 0

    for i in range(1,n):
        if i < R:
            k = i-L

            # case 2 - where zArr[k] is < remaining
            if zArr[k] < R-i+1:
                zArr[i] = zArr[k]

            # case 2b - where zArr[k] is >= remaining
            else:
                while R < n and string[R] == string[R-i]:
                    R += 1

                zArr[i] = R-i
                L = i
                R -= 1

        # case 1
        else:
            L = i
            R = i
            while R < n and string[R] == string[R-i]:
                R +=1
            
            zArr[i] = R-i
            R -= 1

    return zArr