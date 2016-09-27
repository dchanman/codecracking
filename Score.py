#!/usr/bin/env python
import math

class Score:
    
    def __init__(self, file):
        self.loadQuadgrams(file)
    
    def loadQuadgrams(self, file):
        self.score = dict()
        total = 0
        with open(file) as fd:
            for line in fd:
                contents = line.split(' ')
                quad = contents[0].lower()
                score = int(contents[1])
                total += score
                self.score[quad] = score
                if len(self.score) % 100000 == 0:
                    print("Processed {} lines".format(len(self.score)))
        print("Done importing {} scores".format(len(self.score)))
        
        # Process log of probability
        for quad in self.score:
            self.score[quad] = math.log(self.score[quad] / total)
        
        # Absent quad value
        self.absent = math.log(0.01 / total)
    
    def _extractTetragraphs(self, string):
        if len(string) % 2 != 0:
            print("Error. String must be even in length")
            return []
        
        tetragraphs = [string[i:i+4].lower() for i in range(0, len(string) - 3)]
        return tetragraphs
        
    def scoreString(self, string):
        tetragraphs = self._extractTetragraphs(string)
        score = 0
        for tet in tetragraphs:
            if tet in self.score:
                score += self.score[tet]
            else:
                score += self.absent
        
        return score
        
                
if __name__ == "__main__":
    import sys
    score = Score("english_quadgrams.txt")
    # score = Score("small_quad.txt")
    print(score.scoreString(sys.argv[1]))