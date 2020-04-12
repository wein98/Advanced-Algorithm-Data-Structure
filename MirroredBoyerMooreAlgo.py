def getAlphaOrd(letter):
    num = ord(letter.lower())-97

    return num

def badChar(pat, amap, count):
    m = len(pat)

    bcArr = [[-1 for i in range(m)] for j in range(count)]
    # update the badChar table
    # O(km) - m is len(pat), k is number of unique characters in pat
    for i in range(m-1, -1, -1):
        k = amap[getAlphaOrd(pat[i])][1]
        bcArr[k][i] = i
        if i != m-1:
            for j in range(count):
                if j != k:
                    x = bcArr[j][i+1]
                    bcArr[j][i] = x

    print(bcArr)
    return bcArr

class MirroredBoyerMoore(object):

    def __init__(self, pat):
        self.pat = pat
        self.length = len(pat)
        # self.z = zAlgo(pat)

        # count number of unique characters in pat to initialize the size of the table
        # O(m)
        self.amap = [[-1 for i in range(2)] for j in range(26)]
        count = 0
        for i in range(self.length):
            k = getAlphaOrd(self.pat[i])
            if self.amap[k][1] == -1:
                self.amap[k][1] = count
                count += 1
        
        # preprocessing
        self.bad_char_table = badChar(self.pat, self.amap, count) 
        # self.good_suffix_arr = goodSuffix(zAlgo(pat[::-1])[::-1], self.length)  
        # self.matched_prefix_arr = matchedprefix(self.z, self.length)
    
    def badCharRule(self, i, c):
        ci = self.amap[getAlphaOrd(c)][1]

        return self.length-i+1 if self.bad_char_table[ci][i] == -1 else self.bad_char_table[ci][i] - i


patBM = MirroredBoyerMoore("cabcabab")
print(patBM.badCharRule(6, "c"))