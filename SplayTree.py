from collections import deque
from math import floor
class Node:
    def __init__(self, lat, lon, mag, parent):
        self.lat = lat
        self.lon = lon
        self.mag = mag
        self.parent = parent
        self.left = None
        self.right = None

    def setLat(self, lat):
        self.lat = lat

    def setLon(self, lon):
        self.lon = lon
        
    def setMag(self, mag):
        self.mag = mag
        
    def setLeft(self, left):
        self.left = left
    
    def setRight(self, right):
        self.right = right

    def getLat(self):
        return self.lat
    
    def getLon(self):
        return self.lon
    
    def getMag(self):
        return self.mag
    
    def getLeft(self):
        return self.left
    
    def getRight(self):
        return self.right
    
class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, lat, lon, mag):
        if self.root == None:
           self.root = Node(lat, lon, mag, None)
           return

        current = self.root
        while True:
            if mag >= current.getMag():
                if current.getRight() == None:
                    current.setRight(Node(lat, lon, mag, current))
                    self.splay(current.getRight())
                    break
                else:
                    current = current.getRight()
            else:
                if current.getLeft() == None:
                    current.setLeft(Node(lat, lon, mag, current))
                    self.splay(current.getLeft())
                    break
                else:
                    current = current.getLeft()
        return

    def inorder(self):
        lats, lons, mags = [], [], []
        stack = []
        current = self.root

        while current or stack:
            while current:
                stack.append(current)
                current = current.getLeft()

            current = stack.pop()
            lats.append(current.getLat())
            lons.append(current.getLon())
            mags.append(current.getMag())
            current = current.getRight()

        return lats, lons, mags
    
    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        return y

    def rightRotate(self, y):
        x = y.left
        y.left = x.right
        if x.right:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x
        return x

    def splay(self, node):
        while node.parent is not None:
            p = node.parent
            g = p.parent

            if g is None:
                if node == p.left:
                    self.rightRotate(p)
                else:
                    self.leftRotate(p)
            elif node == p.left and p == g.left:
                self.rightRotate(g)
                self.rightRotate(p)
            elif node == p.right and p == g.right:
                self.leftRotate(g)
                self.leftRotate(p)
            elif node == p.left and p == g.right:
                self.rightRotate(p)
                self.leftRotate(g)
            else:
                self.leftRotate(p)
                self.rightRotate(g)
    
    def BFS(self):
        if self.root is None:
            return []

        result = []
        queue = deque()
        queue.append(self.root)

        while queue:
            current = queue.popleft()
            print(current.getMag())
            if current.getLeft() != None:
                print(current.getLeft().getMag())
            if current.getRight() != None:
                print(current.getRight().getMag())
            print("!!!!")

            if current.getLeft():
                queue.append(current.getLeft())

            if current.getRight():
                queue.append(current.getRight())

        return result