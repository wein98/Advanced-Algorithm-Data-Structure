import sys

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

    return(zArr)

# Function that returns the unique number representation of each letter
# O(1) - no iterations
def getAlphaOrd(letter):
    return ord(letter)

# O(km) : m is len(pat), k is number of unique characters in pat
# note - align mismatched bad character
def badChar(pat, amap, count):
    m = len(pat)

    bcArr = [[-1 for i in range(m)] for j in range(count)]
    # update the badChar table
    # O(km) - m is len(pat), k is number of unique characters in pat
    for i in range(m):
        k = amap[getAlphaOrd(pat[i])]
        bcArr[k][i] = i
        if i != 0:
            for j in range(count):
                if j != k:
                    x = bcArr[j][i-1]
                    bcArr[j][i] = x
    return bcArr

# note - align chunk of alpha
# if gsArr[k] == 0, means shift m steps (no mismatch occurs in k before k+1)
def goodSuffix(zSuffix, m):
    # flips pat and get the z-suffix
    # O(m) - m is len(pat)
    gsArr = [0]*(m+1)

    for p in range(m):
        j = m - zSuffix[p]
        gsArr[j] = p 
        
    return gsArr

def matchedprefix(zArr, m):
    z = zArr
    mpArr = [0]*m

    for i in range(m):
        x = z[m-i-1] + m-i-1
        y = m
        if x != y and m-i < m:
            mpArr[m-i-1] = mpArr[m-i]
        else:
            mpArr[m-i-1] = z[m-i-1]

    return mpArr    

class BoyerMoore(object):

    def __init__(self, pat):
        self.pat = pat
        self.length = len(pat)
        self.z = zAlgo(pat)

        # count number of unique characters in pat to initialize the size of the table
        # O(m) - m is len(pat)
        self.amap = [None for j in range(256)]
        count = 0
        for i in range(self.length):
            k = getAlphaOrd(self.pat[i])
            if self.amap[k] == None:
                self.amap[k] = count
                count += 1
        
        # preprocessing
        self.bad_char_table = badChar(self.pat, self.amap, count) 
        self.good_suffix_arr = goodSuffix(zAlgo(pat[::-1])[::-1], self.length)  
        self.matched_prefix_arr = matchedprefix(self.z, self.length)    
    
    def badCharRule(self, i, c):
        # to catch ASCII value that is >255 or the mismatched character from txt doesn't exists in pat
        if getAlphaOrd(c) > 255 or self.amap[getAlphaOrd(c)] == None:
            return i + 1

        ci = self.amap[getAlphaOrd(c)]
        
        # check if need to -1
        return i - self.bad_char_table[ci][i]

    def goodSuffixRule(self, i):
        # case when i+1 > len(pat), return 0 implies ignoring it
        if i >= self.length:
            return 0

        k = self.good_suffix_arr[i]

        # check case if good_suffix_arr[k] == 0, then shift by m - matchedprefec[k+1]
        # denotes the largest suffix == prefix of pat
        # else m - good_suffix_arr[k+1] - 1 
        return self.length - k - 1 if k > 0 else self.length - self.matched_prefix_arr[i]

    # condition when match is found function
    def matchSkip(self):
        return 0 if self.length == 1 else self.length - self.matched_prefix_arr[1]

def search(txt, pat):
    patBM = BoyerMoore(pat)
    m = len(pat)
    n = len(txt)
    j = 0   # pointer in txt
    count = 0
    occurs = 0

    while j <= n-m:
        s = 1   # shift value
        mismatched = False
        resume_val = 0
        pause_val = 0
        k = m-1
        while k >= 0 and k < m:
            if k >= pause_val or k <= resume_val:   # makes sure k is not reprocessing previous processed window of pat
                if not pat[k] == txt[j+k]:
                    s_badChar = patBM.badCharRule(k, txt[j+k])
                    s_goodSuff = patBM.goodSuffixRule(k+1)
                    s = max(s, s_badChar, s_goodSuff)

                    # check if shift value is taken from good suffix rule, then set pause and resume value of k
                    if s_goodSuff >= s_badChar and s_goodSuff >= s:
                        resume_val = k-s
                        pause_val = m-s
                    mismatched = True
                    break
                k -= 1
            else:   # skip to resume value from pause value
                k = resume_val

        if not mismatched:
            s = max(s, patBM.matchSkip())   # do match_skip when pat[1...m] fully matches txt[j...j+m-1]
            # print(j+1)  # print the index where pat matched occurs
            occurs += 1

        j += s
        count+=1
    print(occurs)


if __name__ == "__main__":
    # >>python .\BMalgoImproved.py <text file> <pattern file>
    txtF = sys.argv[1]
    patF = sys.argv[2]
    
    txtF = open(sys.argv[1], "r")
    patF = open(sys.argv[2], "r")

    search(txtF.read(), patF.read())     