# CRC-32 and Weak Collision Resistance

This script iteratively generates strings that look like MD5 hashes and calculates their CRC checksums. When a checksum equal to a specified checksum is found, the program notifies the user and terminates.

Usage:
```
python3 target.py STARTNUM ENDNUM
```

For faster results, run multiple processes on multiple machines and have them search different ranges of numbers.