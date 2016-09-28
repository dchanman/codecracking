#!/usr/bin/env python

# Uses Simluated Annealing
# https://en.wikipedia.org/wiki/Simulated_annealing

from Playfair import Playfair
from Score import Score
import random
import math

class CrackerOutput:
    def __init__(self, score, key, plaintext):
        self.score = score
        self.key = key
        self.plaintext = plaintext
    
    def __str__(self):
        return "Score: {}\nKey: {}\n{}".format(self.score, self.key, self.plaintext)

class Cracker:
    
    def __init__(self, ciphertext, key = None):
        self.score = Score("english_quadgrams.txt")
        self.key = "DPQMKEGXTUVNOLZAIBFHWSRCY" if key is None else key
        self.playfair = Playfair(self.key)
        self.ciphertext = ciphertext
        
        self.temperature = 10 + 0.087 * (len(ciphertext) - 84);
        
        self.currentBestOutput = self.crackAndScore()
        
    
    def crackAndScore(self):
        plaintext = self.playfair.decipherStr(self.ciphertext)
        return CrackerOutput(self.score.scoreString(plaintext), self.key, plaintext)
    
    def newBestOutput(self, newOutput):
        self.currentBestOutput = newOutput
        self.key = self.playfair.keyMatrixToString()
        print(newOutput)
    
    def round(self):
        self.playfair.generateNextKey()
        crackerOutput = self.crackAndScore()
        scoreDiff = self.currentBestOutput.score - crackerOutput.score
        if scoreDiff < 0:
            self.newBestOutput(crackerOutput)
            return True
        else:
            # According to the Simulated Annealing algorithm, once in a while, we will take an inferior key
            rand = random.randint(1,1000) / 1000
            chance = 1 / math.exp(scoreDiff / self.temperature)
                        
            if chance > rand:
                print("Rand: {}, Chance: {}, Temp: {}, Diff: {}".format(rand, chance, self.temperature, scoreDiff))
                self.newBestOutput(crackerOutput)
                return True
            
            # Reset the key, thus keeping the parent key
            self.playfair = Playfair(self.key)
            return False

if __name__ == "__main__":
    import sys
    
    ciphertext = sys.argv[1]
    key = None
    if len(sys.argv) > 2:
        key = sys.argv[2]
    
    cracker = Cracker(ciphertext, key)
    while cracker.temperature > 30:
        for i in range(50000):
            cracker.round()
        cracker.temperature -= 10
    
    output = cracker.crackAndScore()
    print(output)