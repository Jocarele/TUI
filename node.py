class Node():
    def __init__(self, value,children = None):
        self.value = value
        self.children = children

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        if (self.children != None):
            for child in self.children:
                ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'
    
    def makeChildren(self,node):
        if(self.children == None):
            self.children = [node]
        else:
            self.children.append(node)
        