# Chia Wei Ying
# 30113199

class HuffmanTree:
    def __init__(self):
        self.root = self.Node()

    class Node:
        def __init__(self):
            self.leaf = False
            self.left = None
            self.right = None
            self.char = None

    def insertNode(self, value, path):
        currNode = self.root

        for i in range(len(path)):
                
            if path[i] == '1': # traverse to left child
                if currNode.right is None:
                    currNode.right = self.Node()
                currNode = currNode.right
            else:
                if currNode.left is None:
                    currNode.left = self.Node()
                currNode = currNode.left

            if i == len(path)-1:
                currNode.leaf = True
                currNode.char = value
    
    def getChar(self, currNode, huffman):
        currNode = self.root

        for i in range(len(huffman)):
            if huffman[i] == '1':
                currNode = currNode.left
            else:
                currNode = currNode.right

        if currNode.leaf:
            return currNode.char

    def getNode(self, prevNode, huffman):
        if huffman == '1':
            return prevNode.right
        else:
            return prevNode.left