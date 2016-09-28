#!/usr/bin/env python

import zlib
import time
import string
import sys

def bytesToString(num):
    bytes = [hex(num >> i & 0xff) for i in (24,16,8,0)]
    return "".join(bytes)

def intToMD5String(num):
    return "{:032X}".format(num)

startNum = int(sys.argv[1])
endNum = int(sys.argv[2])

goal = zlib.crc32("45287151bebf4eb44138594de0353d0b".encode("ascii"), 0)

print("Goal: {}".format(hex(goal)))
    
startTime = time.time()
print("{}: Starting search...".format(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))

i = startNum
while i < endNum:
    md5 = intToMD5String(i)
    crc = zlib.crc32(md5.encode("utf-8"), 0)
    # print("{} ({}): {} (!={})".format(i, hex(i), hex(crc), hex(goal)))
    if crc == goal:
        print("Found {} ({}) == crc32(33184128)".format(i, md5))
        break
    i += 1
    count = i - startNum
    if count % 1000000 == 0:
        print("{}: Searched {}, {}".format(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()), count, md5))

print("{}: Done!".format(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
endTime = time.time()
elapsedTime = endTime - startTime
print("Required {} seconds".format(elapsedTime))
print("Made {} checks".format(count))
