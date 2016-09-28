# Playfair Solver using Simulated Annealing

The algorithm used to solve Playfair was outlined by Michael J. Cowan in his 2008 paper *Breaking Short Playfair Ciphers with the Simulated Annealing Algorithm*. His paper can be found here: http://www.tandfonline.com/doi/full/10.1080/01611190701743658

The scoring system comes from James Lyons's Practical Cryptography website (http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/), and the english_quadgrams.txt file is downloaded from his article on *Quadgram Statistics as a Fitness Measure*.

## Usage
```
python3 Cracker.py CIPHERTEXT [KEY]
```
