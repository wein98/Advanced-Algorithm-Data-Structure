class ImplicitST (object):
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.root = None
        self.endPointer = EndPointer()
        self.j = 0
        self.activeNode = None
        self.activeEdge = -1
        self.lastNewNode = None
        self.activeLength = 0
        self.edgeCount = 0

        self.buildSuffixTree()
        
    "Function to get letter's ascii code"
    def getAlphaOrd(self, x):
        return ord(x) - 32

    "Function to create new node."
    def newNode(self, start, end, leaf=True):
        node = Node(start, end, leaf)
        node.suffixLink = self.root
        return node

    def extendSuffixTree(self, i):
        "Extension Rule 1, trick 4 - rapid leaf extension trick"
        self.endPointer.setEnd(i)   # set end pointer to i
        self.lastNewNode = None     # new phase has no last new node

        while (self.j <= i):
            if (self.activeLength == 0): # previous phase wasn't a showstopper
                self.activeEdge = i

            # Condition when active_length == 0 and in extension rule 2
            if(self.activeNode.getChildren(self.getAlphaOrd(self.data[self.activeEdge])) is None):
                "Extension Rule 2 - a new edge is created"
                self.activeNode.addChild(self.getAlphaOrd(self.data[self.activeEdge]), self.newNode(i, self.endPointer))
                self.edgeCount += 1
                if i == self.j:    
                    self.j += 1
            else:
                if self.activeLength > 0:
                    # When there's an active_edge and active_length
                    pointer = self.activeEdge + self.activeLength

                    if not self.data[i] == self.data[pointer]:
                        "Extension Rule 2 - creating internal node"
                        # split edge and update the first part of the edge
                        edge = self.activeNode.getChildren(self.getAlphaOrd(self.data[self.activeEdge]))
                        edge.end = self.activeEdge + self.activeLength-1
                        edge.setNonLeaf()
                        # insert new internal node
                        node = self.newNode(edge.end+1, self.endPointer)
                        edge.addChild(self.getAlphaOrd(self.data[edge.end+1]), node)
                        # add a branch at this internal node with new character of phase i
                        edge.addChild(self.getAlphaOrd(self.data[i]), self.newNode(i, self.endPointer))

                        self.edgeCount += 2

                        if not self.lastNewNode is None:    # link last new node to this new internal node
                            self.lastNewNode.suffixLink = edge
                        self.lastNewNode = edge  # update lastNewNode to this new internal node

                        self.j += 1

                        "Trick 2 - skip/count trick (more efficient than lecture slides)"
                        if not self.activeNode is self.root:
                            # traverse via suffix link
                            self.activeNode = self.activeNode.suffixLink
                            self.activeEdge = self.activeNode.getChildren(self.getAlphaOrd(self.data[self.activeEdge])).start
                            continue

                        self.activeLength -= 1

                        if self.activeLength > 0:   # update new active_edge from the active_node
                            self.activeEdge = self.activeNode.getChildren(self.getAlphaOrd(self.data[self.j])).start
                        
                        continue    # go to next j in same phase i

                "Extension Rule 3 - new character extension exist before, do nothing"
                
                "Trick 3 - showstopper, j is not increasing"
                currentEdgeEnd = self.activeNode.getChildren(self.getAlphaOrd(self.data[self.activeEdge])).getEnd()
                currentEdgeStart = self.activeNode.getChildren(self.getAlphaOrd(self.data[self.activeEdge])).start
                self.activeLength += 1

                if(currentEdgeEnd - currentEdgeStart + 1 < self.activeLength):
                    # an internal node is found in Extension Rule 3
                    # update new active node and active edge
                    self.activeNode = self.activeNode.getChildren(self.getAlphaOrd(self.data[self.j]))
                    self.activeEdge = self.activeNode.getChildren(self.getAlphaOrd(self.data[currentEdgeEnd+1])).start
                    self.activeLength = 1
                else:
                    self.activeEdge = currentEdgeStart
                break  


    def buildSuffixTree(self):
        "Root node has a start and end indices as -1"
        self.root = self.newNode(-1, -1, False)
        self.root.suffixLink = self.root
        self.activeNode = self.root # first activeNode is root
        
        for i in range(self.size):
            self.extendSuffixTree(i)
 
class Node (object):
    def __init__(self, start, end, leaf=True):
        self.children = None
        self.suffixLink = None
        self.leaf = leaf
        # Trick 1 - space-efficient representation of edge-labels/substrings
        self.start = start
        self.end = end

        if not leaf:
            self.setNonLeaf()

    "Return children node in position i"
    def getChildren(self, i):
        return self.children[i]

    "Add a node to this.children"
    def addChild(self, i, child):
        self.children[i] = child

    "Change this node from leaf to non leaf"
    def setNonLeaf(self):
        self.children = [None]*96

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

suffixtree = ImplicitST("abcabxabcyab")