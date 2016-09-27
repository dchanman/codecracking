#!/usr/bin/env python

# Playfair cracker
from functools import reduce
import random
import copy

class Coords:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        
    def __str__(self):
        return "({}, {})".format(self.col, self.row)

class KeyGen:
    def flipDiagonal(keyMatrix):
        newMatrix = [[keyMatrix[x][y] for x in range(5)] for y in range(5)]
        return newMatrix
    
    def flipTopBottom(keyMatrix):
        newMatrix = [[keyMatrix[5 - y - 1][x] for x in range(5)] for y in range(5)]
        return newMatrix
    
    def flipLeftRight(keyMatrix):
        newMatrix = [[keyMatrix[y][5 - x - 1] for x in range(5)] for y in range(5)]        
        return newMatrix
    
    def swapTwoRows(keyMatrix, row1, row2):
        newMatrix = copy.deepcopy(keyMatrix)
        newMatrix[row1] = keyMatrix[row2]
        newMatrix[row2] = keyMatrix[row1]
        return newMatrix
    
    def swapTwoCols(keyMatrix, col1, col2):
        newMatrix = copy.deepcopy(keyMatrix)
        for i in range(5):
            newMatrix[i][col1] = keyMatrix[i][col2]
            newMatrix[i][col2] = keyMatrix[i][col1]
        return newMatrix
    
    def swapTwoCoords(keyMatrix, coord1, coord2):
        newMatrix = copy.deepcopy(keyMatrix)
        newMatrix[coord1.row][coord1.col] = keyMatrix[coord2.row][coord2.col]
        newMatrix[coord2.row][coord2.col] = keyMatrix[coord1.row][coord1.col]
        return newMatrix
        
    def generateNextKey(keyMatrix):
        # Using the simplified simulated annealing algorithm provided by Michael J Cowan in
        # "Breaking Short Playfair Ciphers with the Simulated Annealing Algorithm"
        rand = random.randint(1, 50)
        if rand == 1:
            return KeyGen.flipDiagonal(keyMatrix)
        elif rand == 2:
            return KeyGen.flipTopBottom(keyMatrix)
        elif rand == 3:
            return KeyGen.flipLeftRight(keyMatrix)
        elif rand == 4:
            return KeyGen.swapTwoCols(keyMatrix, random.randint(0, 4), random.randint(0, 4))
        elif rand == 5:
            return KeyGen.swapTwoRows(keyMatrix, random.randint(0, 4), random.randint(0, 4))
        else:
            return KeyGen.swapTwoCoords(keyMatrix, Coords(random.randint(0, 4), random.randint(0, 4)), Coords(random.randint(0, 4), random.randint(0, 4)))
        
class Playfair:
    def __init__(self, key):
        if len(key) != 25:
            print("ERROR: Key must be 25 characters in length")
            return None
        
        self.keyMatrix = [[0 for x in range(5)] for y in range(5)]
        self.currentKeyAttempts = 0
        
        count = 0
        for a in key:
            col = int(count / 5)
            row = int(count % 5)
            self.keyMatrix[col][row] = a
            count += 1
            
    def printMatrix(self, matrix = None):
        matrix = self.keyMatrix if matrix is None else matrix
        for row in matrix:
            print(row)
    
    def keyMatrixToString(self, matrix = None):
        matrix = self.keyMatrix if matrix is None else matrix
        return "".join(["".join(row) for row in matrix])
    
    def generateNextKey(self):
        self.keyMatrix = KeyGen.generateNextKey(self.keyMatrix)
    
    def findCoord(self, letter):
        cols = [row.index(letter) if letter in row else -1 for row in self.keyMatrix]
        # Huge hack. All entries will be -1 except for one.
        # eg. [-1, -1, 2, -1, -1]
        # reduce() will sum all the entries, +4 will remove all of the -1s
        # eg. -1 + -1 + 2 + -1 + -1 + 4 = 2
        row = reduce(lambda x,y: x + y, cols) + 4
        # Huge hack part 2. Find the entry that is not -1
        col = list(map(lambda x: x == -1, cols)).index(False)
        
        return Coords(col, row)
    
    def encipher(self, digraph):
        a = digraph[0]
        b = digraph[1]
        coordA = self.findCoord(a)
        coordB = self.findCoord(b)
        newA = a
        newB = b
        
        if coordA.row == coordB.row:
            # Case 1: Same row
            newA = self.keyMatrix[coordA.row][(coordA.col + 1) % 5]
            newB = self.keyMatrix[coordB.row][(coordB.col + 1) % 5]
                    
        elif coordA.col == coordB.col:
            # Case 2: Same col
            newA = self.keyMatrix[(coordA.row + 1) % 5][coordA.col]
            newB = self.keyMatrix[(coordB.row + 1) % 5][coordB.col]
        else:
            # Case 3: Rectangle
            newA = self.keyMatrix[coordA.row][coordB.col]
            newB = self.keyMatrix[coordB.row][coordA.col]
        
        return newA + newB

    def decipher(self, digraph):
        a = digraph[0]
        b = digraph[1]
        coordA = self.findCoord(a)
        coordB = self.findCoord(b)
        newA = a
        newB = b
        
        if coordA.row == coordB.row:
            # Case 1: Same row
            newA = self.keyMatrix[coordA.row][(coordA.col - 1) % 5]
            newB = self.keyMatrix[coordB.row][(coordB.col - 1) % 5]
                    
        elif coordA.col == coordB.col:
            # Case 2: Same col
            newA = self.keyMatrix[(coordA.row - 1) % 5][coordA.col]
            newB = self.keyMatrix[(coordB.row - 1) % 5][coordB.col]
        else:
            # Case 3: Rectangle
            newA = self.keyMatrix[coordA.row][coordB.col]
            newB = self.keyMatrix[coordB.row][coordA.col]
        
        return newA + newB

    def encipherStr(self, string):
        digraphs = []
        i = 0
        while i < len(string):
            if i + 1 == len(string):
                string += "x"
            elif string[i] == string[i+1]:
                string = string[:i + 1] + "x" + string[i + 1:]
            digraphs.append(string[i:i+2])
            i += 2

        return "".join([self.encipher(digraph) for digraph in digraphs])

    def decipherStr(self, string):
        if len(string) % 2 != 0:
            print("Error: String needs to have an even number of characters")
        digraphs = []
        i = 0
        while i < len(string):
            digraphs.append(string[i:i+2])
            i += 2
        return "".join([self.decipher(digraph) for digraph in digraphs])

if __name__ == "__main__":
    import sys
    
    PF = Playfair("abcdefghijklmnopqrstuvwxy")
    PF.printMatrix()
    # print()
    # val = "sx"
    # enciphered = PF.encipher(val)
    # deciphered = PF.decipher(enciphered)
    # print(val)
    # print(enciphered)
    # print(deciphered)
    # 
    # print()
    # enc = PF.encipherStr(sys.argv[1])
    # dec = PF.decipherStr(enc)
    # print("Enc: {}".format(enc))
    # print("Dec: {}".format(dec))
    print()
    new = KeyGen.generateNextKey(PF.keyMatrix)
    PF.printMatrix(new)
    key2 = PF.keyMatrixToString(new)
    print(key2)
    PF2 = Playfair(key2)
    PF2.printMatrix()