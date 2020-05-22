# Chia Wei Ying
# 30113199

import sys
from Ukkonen import * # put Ukkonen.py in the same directory as this file

class BWT:
    def __init__(self, _txt):
        self.txt = _txt
        self.len = len(_txt)
        self.sufftrie = ImplicitST(_txt)
        self.suffArr = []
        self.nodeTraverse(self.sufftrie.root)

        result = ""
        for i in range(len(self.suffArr)):
            result += self.txt[self.suffArr[i]-1]

        self.output(result)

    "Write output to output_bwt.txt"
    def output(self, result):
        outF = open("output_bwt.txt", "a")
        outF.write(result+"\n")
        
    "suffix trie DFS"
    def nodeTraverse(self, n):
        for i in range(96):
            x = n.getChildren(i)                
            if not x is None and x.leaf:
                self.suffArr.append(x.j)
            elif not x is None:
                self.nodeTraverse(x)

if __name__ == "__main__":
    # >>python .\suffixtreeBWT.py <text file> 
    outF = open("output_bwt.txt", "w+")
    txtF = open(sys.argv[1], "r")
    
    for line in txtF:
        BWT(line+"$")