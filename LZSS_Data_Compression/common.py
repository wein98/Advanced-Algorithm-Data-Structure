# Chia Wei Ying
# 30113199

# convert ASCII char to bitstring
def ASCIItoBin(x):
    return getASCIIbin(ord(x))

# get ASCII value in dec
def getOrd(x):
    return ord(x)

# convert decimal to bitstring
def bitStringConversion(dec):
    if dec == 1:
        return "1"
    if dec % 2 == 0:
        return "0" + bitStringConversion(dec//2)
    else:
        return "1" + bitStringConversion(dec//2)

def getASCIIbin(dec):
    x = bitStringConversion(dec)
    if len(x) < 7:
        pad = '0'*(7-len(x))
        x += pad
    return x[::-1]

# reverse the result from bitStringConversion(dec)
# O(log n) - n = dec
def getBinary(dec):
    return bitStringConversion(dec)[::-1]

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