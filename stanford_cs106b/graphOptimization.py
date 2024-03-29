# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 12:56:06 2015

@author: george
"""

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return str(self.src) + '->' + str(self.dest)

class WeightedEdge(Edge):
    def __init__(self, src, dest, weight = 1.0):
        self.src = src
        self.dest = dest
        self.weight = weight
    def getWeight(self):
        return self.weight
    def __str__(self):
        return str(self.src) + '->(' + str(self.weight) + ')'\
            + str(self.dest)

class Digraph(object):
    def __init__(self):
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = res + str(k) + '->' + str(d) + '\n'
        return res[:-1]

class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)


def printPath(path):
    # a path is a list of nodes
    result = ''
    for i in range(len(path)):
        if i == len(path) - 1:
            result = result + str(path[i])
        else:
            result = result + str(path[i]) + '->'
    return result


#nodes = []
#nodes.append(Node("ABC")) # nodes[0]
#nodes.append(Node("ACB")) # nodes[1]
#nodes.append(Node("BAC")) # nodes[2]
#nodes.append(Node("BCA")) # nodes[3]
#nodes.append(Node("CAB")) # nodes[4]
#nodes.append(Node("CBA")) # nodes[5]
#
#g = Graph()
#for n in nodes:
#    g.addNode(n)
#
#g.addEdge(Edge(nodes[0],nodes[1]))
#g.addEdge(Edge(nodes[0],nodes[2]))
#g.addEdge(Edge(nodes[1],nodes[4]))
#g.addEdge(Edge(nodes[2],nodes[3]))
#g.addEdge(Edge(nodes[3],nodes[5]))
#g.addEdge(Edge(nodes[4],nodes[5]))
#
#print(printPath(nodes))

import random
g = Graph() 
n = 5

def newNode(name):
    name = Node(name)
    return name
    
def addEdge(x,y):
    g.addEdge(Edge(x,y))
    return
        
nodes = []
for i in range(n):
    nodes.append(newNode(i)) # newNode takes one parameter, the number of the node
    
for n in nodes:
    g.addNode(n)

#for i in range(len(nodes)):
#    x = random.choice(nodes)
#    y = random.choice(nodes)
#    addEdge(x,y)    

#for i in range(len(nodes)):
#	x = random.choice(nodes)
#	y = random.choice(nodes)
#	addEdge(x,y)
#	addEdge(y,x)

for i in range(len(nodes)):
	w = random.choice(nodes)
	x = random.choice(nodes)
	y = random.choice(nodes)
	z = random.choice(nodes)
	addEdge(w,x)
	addEdge(x,y)
	addEdge(y,z)
	addEdge(z,w)



   
for n in nodes:
    print ('parent:', n.getName())
    for i in g.childrenOf(n):
        print ('children:', i.getName())
    print ('-------')
