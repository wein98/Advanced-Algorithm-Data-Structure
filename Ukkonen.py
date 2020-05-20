"Function to get letter's ascii code"
def getOrd(x):
    return ord(x) - 32

class ImplicitST (object):
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.root = None
        self.endPointer = EndPointer()
        self.j = 0
        self.activeNode = None
        self.activeEdge = -1
        self.prevNode = None
        self.activeLength = 0

        self.buildSuffixTree()

    "Function to create new node."
    def newNode(self, start, end, j, leaf=True):
        node = Node(start, end, j, leaf)
        node.suffixLink = self.root
        return node

    def extendSuffixTree(self, i):
        "Extension Rule 1"
        "Trick 4 - rapid leaf extension trick"
        self.endPointer.setEnd(i)
        self.prevNode = None    # set prevNode to None when entering a new phase

        while(self.j <= i):
            if self.activeLength == 0:
                self.activeEdge = i
            
            "Extension Rule 2 - branch new leaf from existing node"
            if self.activeNode.getChildren(getOrd(self.data[self.activeEdge])) is None:
                self.activeNode.addChild(getOrd(self.data[self.activeEdge]), self.newNode(i, self.endPointer, self.j))

                # create suffixlink if there is an internal node branching leaf from last extension in same phase
                if self.prevNode is not None:
                    self.prevNode.suffixLink = self.activeNode
                    self.prevNode = None
            
            else: # There exists an outgoing activeEdge from activeNode
                _next = self.activeNode.getChildren(getOrd(self.data[self.activeEdge]))
                length = _next.getEdgeLen()

                # traverse to an internal node, update new activeNode
                if self.activeLength >= length: 
                    self.activeNode = _next
                    self.activeEdge += length
                    self.activeLength -= length
                    continue

                "Extension Rule 3"
                if self.data[i] == self.data[_next.start + self.activeLength]:
                    if self.prevNode is not None and self.activeNode is not self.root:
                        self.prevNode.suffixLink = self.activeNode
                        self.prevNode = None
                    
                    self.activeLength += 1
                    break   # Trick 3 - showstopper

                "Extension Rule 2 - create new internal node"
                _start = _next.start
                _next.start += self.activeLength
                # New internal node
                newNode = self.newNode(_start, _start+self.activeLength-1, None, False)
                newNode.addChild(getOrd(self.data[_next.start]), _next)
                newNode.addChild(getOrd(self.data[i]), self.newNode(i, self.endPointer, self.j))
                # activeNode connect to this new internal node
                self.activeNode.children[getOrd(self.data[_start])] = newNode

                # create suffixLink to this newly created internal node if there was any internal
                # node created in last extensions of the same phase 
                if self.prevNode is not None:   
                    self.prevNode.suffixLink = newNode
                self.prevNode = newNode

            self.j += 1

            # update activeLength and activeEdge for next extension
            if self.activeNode is self.root and self.activeLength > 0:
                self.activeLength -= 1
                self.activeEdge = self.j

            else:
                # traverse to suffixLink
                self.activeNode = self.activeNode.suffixLink    

    def buildSuffixTree(self):
        "Root node has a start and end indices as -1"
        self.root = self.newNode(-1, -1, None, False)
        self.root.suffixLink = self.root
        self.activeNode = self.root # first activeNode is root
        
        for i in range(self.size):
            self.extendSuffixTree(i)

class Node (object):
    def __init__(self, start, end, j, leaf=True):
        self.children = None
        self.suffixLink = None
        self.leaf = leaf
        "Trick 1 - space-efficient representation of edge-labels/substrings"
        self.start = start
        self.end = end
        self.childCount = 0
        self.j = j

        if not leaf:
            self.setNonLeaf()

    "Return children node in position i"
    def getChildren(self, i):
        return self.children[i]

    "Add a node to this.children"
    def addChild(self, i, child):
        self.childCount += 1
        self.children[i] = child

    "Change this node from leaf to non leaf"
    def setNonLeaf(self):
        self.leaf = False
        self.j = None
        self.children = [None]*96

    "Get length of edge"
    def getEdgeLen(self):
        return self.getEnd() - self.start + 1 

    "Return self.end"
    def getEnd(self):
        return self.end if isinstance(self.end, int) else self.end.getEnd()

class EndPointer:
    def __init__(self):
        self.value = None

    def setEnd(self, end):
        self.value = end

    def getEnd(self):
        return self.value