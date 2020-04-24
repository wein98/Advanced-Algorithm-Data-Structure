import sys

# Normal z-algo function
def zAlgo(pat):
    n = len(pat)
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
                while R < n and pat[R] == pat[R-i]:
                    R += 1

                zArr[i] = R-i
                L = i
                R -= 1
        
        # case 1
        else:
            L = i
            R = i
            while R < n and pat[R] == pat[R-i]:
                R +=1
            
            zArr[i] = R-i
            R -= 1

    return zArr

class wildcardMatch(object):
    def __init__(self, txt, pat):
        # initializations
        self.pat = pat
        self.txt = txt
        self.txtLen = len(txt)
        self.segmentsArr = self.getSegments()
        self.currentSegZ = []
        self.previousSegZ = []
        self.mergeLen = 0
        self.segmentLen = 0
        self.cumLen = 0
        self.noMatch = False

        # 1. gets the segments of pat in self.getSegments() and store it in self.segmentsArr
        # 2. for each self.segmentsArr
        #       a) if segment is characters, do zAlgo on this segment and go to merge(), else go to freemerge()
        #       b) if self.noMatch is True, break
        # 3. print output in self.outputFile()
        # O(m + nm + n)

        # operations
        self.match()
        self.outputFile()


    # Function that returns an array of segments between characters and '?' in pat
    # "de??du?" -> ['de', -2, 'du', -1]
    # O(m) - m is len(pat)
    def getSegments(self):
        m = len(self.pat)
        x = []
        i = 0
        k = 0
        y = ""
        
        while i < m:
            if not self.pat[i] == '?':
                if k >= 0:
                    y += self.pat[i]
                    k += 1
                else:
                    x.append(k)
                    y = ""
                    y += self.pat[i]
                    k = 1
            else:
                if k < 0:
                    k -= 1
                else:
                    if i != 0:
                        x.append(y)
                    k = -1
            i += 1
        if k > 0:
            x.append(y)
        else:
            x.append(k)

        return x

    # Function that merge a previous computed segment with the length of new zalgo segment of characters
    # O(n) - n is len(txt)
    def merge(self):
        x = [0]*self.txtLen
        k = self.cumLen + self.segmentLen   # represents the max length matched after merge
        matched = False

        for i in range(self.txtLen):
            if i + k > self.txtLen: # stop looping if the remaining is < length after merged
                break
            
            if self.previousSegZ[i] == self.cumLen:
                if self.currentSegZ[i+self.cumLen+self.segmentLen+1] == self.segmentLen:
                    matched = True
                    x[i] = k

        # a no match found pointer to stop comparing further segments
        if not matched:
            self.noMatch = True

        self.previousSegZ = x   # make this as previous segment of Z

    # Function that merges previous processed zarray to length of '?'
    # O(n) - n is len(txt)
    def freeMerge(self):
        x = [0]*self.txtLen
        k = self.cumLen - self.mergeLen # represents the max length matched after merge

        # this handle the case when first segment is characters segment where the array is not in
        # size of n, so when merging, it needs a shift of s
        s = 0
        if len(self.previousSegZ) > self.txtLen:
            s = len(self.previousSegZ) - self.txtLen

        for i in range(s, self.txtLen):
            if i-s + k > self.txtLen:   # stop looping if the remaining is < length after merged
                break

            if self.previousSegZ[i] == self.cumLen:  # update wanted length
                x[i-s] = k
        
        self.previousSegZ = x   # make this as previous segment of Z
  
    # Main function to do the matching
    # O(k(n+m/k)) - k is total number of segments, n is len(txt), m is len(pat)
    def match(self):
        for i in range(len(self.segmentsArr)):
            if self.noMatch:    # stop matching further segments, if previous segment hasn't found a match
                break

            if isinstance(self.segmentsArr[i], str):    # when segment is characters
                x = self.segmentsArr[i] + "$" + self.txt
                self.segmentLen = len(self.segmentsArr[i])

                if not i == 0:
                    self.currentSegZ = zAlgo(x)
                    self.merge()
                else:
                    self.previousSegZ = zAlgo(x)

                self.cumLen += self.segmentLen
            else:   # when segment is '?'
                if not i == 0:
                    self.mergeLen = self.segmentsArr[i]
                    self.freeMerge()
                else:
                    self.previousSegZ = [-self.segmentsArr[0]]*self.txtLen
                self.cumLen += -self.segmentsArr[i]

    
    # Function that prints an output file named "output_wildcard_matching.txt"
    # O(n-m) - n is len(txt) and m is len(pat)
    def outputFile(self):
        f = open("output_wildcard_matching.txt", "w+")
        m = len(self.pat)
        if not self.noMatch:
            for i in range(len(self.previousSegZ)-m+1):
                if self.previousSegZ[i] == m:
                    f.write("%d\n" % (i+1))

if __name__ == "__main__":
    # >>python .\wildcard_matching.py <text file> <pattern file>
    txtF = sys.argv[1]
    patF = sys.argv[2]
    
    txtF = open(sys.argv[1], "r")
    patF = open(sys.argv[2], "r")

    wildcardMatch(txtF.read(), patF.read())    