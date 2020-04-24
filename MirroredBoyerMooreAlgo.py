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

    return zArr

# Function that returns the unique number representation of each letter
# O(1) - no iterations
def getAlphaOrd(letter):
    return ord(letter)

# Function that create and returns table of bad character rule for pat
# O(m) - m is len(pat)
def badChar(pat, amap, count):
    m = len(pat)

    bcArr = [[-1 for i in range(m)] for j in range(count)]
    # update the badChar table
    # O(km) - m is len(pat), k is number of unique characters in pat
    for i in range(m-1, -1, -1):
        k = amap[getAlphaOrd(pat[i])]
        bcArr[k][i] = i
        if i != m-1:
            for j in range(count):
                if j != k:
                    x = bcArr[j][i+1]
                    bcArr[j][i] = x
    return bcArr

# O(m) - m is len(pat)
def goodPrefix(z, m):
    x = [0]*(m+1)

    for p in range(m):
        j = m - z[p]
        x[j] = p 
        
    return x

# Function that preprocess pat for matched suffix rule needed in good prefix rule and matchSkip()
# O(M) - m is len(pat)
def matchedSuffix(zArr, m):
    z = zArr
    msArr = [0]*m

    for i in range(m):
        x = z[i] + m-i-1
        y = m
        if x != y and i > 0:
            msArr[i] = msArr[i-1]
        else:
            msArr[i] = z[i]

    return msArr

class MirroredBoyerMoore(object):

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
        # big O will be stated in each respective called function
        self.bad_char_table = badChar(self.pat, self.amap, count) 
        self.good_prefix_arr = goodPrefix(zAlgo(pat)[::-1], self.length)[::-1]
        self.matched_suffix_arr = matchedSuffix(self.z[::-1], self.length)
    
    # Function that returns shift value based on bad character rule
    # O(1) - no iterations
    def badCharRule(self, i, c):
        # to catch ASCII value that is >255 or the mismatched character from txt doesn't exists in pat
        if getAlphaOrd(c) > 255 or self.amap[getAlphaOrd(c)] == None:
            return self.length-i-1
        
        ci = self.amap[getAlphaOrd(c)]

        return self.length-i+1 if self.bad_char_table[ci][i] == -1 else self.bad_char_table[ci][i] - i

    # Function that returns shift value based on good prefix rule
    # O(1) - no iterations
    def goodPrefixRule(self, i):
        k = self.good_prefix_arr[i]
        # return self.length - k if k > 0 else ignore
        return self.length - k - 1 if k > 0 else self.length - self.matched_suffix_arr[i]
    
    # Function deals with condition when match is found.
    # O(1) - no iteration
    def matchSkip(self):
        return 0 if self.length == 1 else self.length - self.matched_suffix_arr[self.length-2]

# O(n) - n is len(txt) 
# where len(pat) == 1 and each character in txt[1...n] is pat[0] 
def printOccurences(occur):
    n = len(occur)
    for i in range(n):
        print(occur[n-i-1])

def search(txt, pat):
    patBM = MirroredBoyerMoore(pat)
    m = len(pat)
    n = len(txt)
    occurencces = []
    j = n-m-1   # pointer in txt
    count = 0

    while j >= 0:
        s = 1   # shift value
        mismatched = False
        resume_val = 0
        pause_val = 0
        k = 0   # pointer in pat
        
        while k >= 0 and k < m:
            if k <= pause_val or k >= resume_val:   # makes sure k is not reprocessing previous processed window of pat
                if not pat[k] == txt[j+k]:
                    s_badChar = patBM.badCharRule(k, txt[j+k])
                    s_goodPref = patBM.goodPrefixRule(k)
                    s = max(s, max(s_badChar, s_goodPref))

                    # check if shift value is taken from good prefix rule, then set pause and resume value of k
                    if s_goodPref >= s_badChar and s_goodPref >= s:
                        if k+s-1 >= m:
                            resume_val = k
                        else:
                            resume_val = k+s-1
                        pause_val = s-1
                    mismatched = True
                    break
                k += 1
            else:   # skip to resume value from pause value
                k = resume_val

        if not mismatched:
            s = max(s, patBM.matchSkip())   # do match_skip when pat[1...m] fully matches txt[j...j+m-1]
            occurencces.append(j+1)     # append ocurrence index to occurencces[]

        j -= s
        count += 1

    print(count)
    print(len(occurencces))
    # printOccurences(occurencces)
    
if __name__ == "__main__":
    # >>python .\MirroredBoyerMoore.py <text file> <pattern file>
    txtF = sys.argv[1]
    patF = sys.argv[2]
    
    txtF = open(sys.argv[1], "r")
    patF = open(sys.argv[2], "r")

    search(txtF.read(), patF.read()) 