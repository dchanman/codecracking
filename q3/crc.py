#!/usr/bin/env python

import zlib
import time
import random
import string

def intToMD5String(num):
    return "{:032X}".format(num)

history = dict()

startTime = time.time()
print("{}: Starting search...".format(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))

while True:
    # if len(history) % 1000 == 0:
        # print("{}: Searched {}".format(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()), len(history)))
    # randomString = intToMD5String(random.randint(0, 4294967296))
    randomString = intToMD5String(len(history))
    crc = zlib.crc32(randomString, 0)
    if crc in history and history[crc] != randomString:
         print("FOUND COLLISION:")
         print(history[crc])
         print(randomString)
         break
    else:
        history[crc] = randomString
    
print("{}: Done!".format(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
endTime = time.time()
elapsedTime = endTime - startTime
print("Required {} seconds".format(elapsedTime))
print("Computed {} checksums".format(len(history)))

# Sun, 25 Sep 2016 23:09:25: Searched 150000
# FOUND COLLISION: 36964ERCO7C8IF07EL59D45JFDUICI8V and V6OX6DXR9C1ZMD5ABB35LITY9MZ18Q5X
# Sun, 25 Sep 2016 23:09:25: Done!
# Required 71.8803510666 seconds
# 
# real	1m11.966s
# user	0m54.776s
# sys	0m17.160s
# 
# Sun, 25 Sep 2016 23:11:19: Searched 175000
# FOUND COLLISION: YGCPSFH5PC33Q29H1A9Q8PJQ43LY3ZAF and 092XR1KW2U0C93XWBGGYQU039457JD7A
# Sun, 25 Sep 2016 23:11:19: Done!
# Required 93.303789854 seconds
# 
# real	1m33.405s
# user	1m12.032s
# sys	0m21.100s
# 
# Sun, 25 Sep 2016 23:12:47: Searched 51000
# FOUND COLLISION: YT8JWX43BGGD4T5A44QN3LVF6BSI4BU5 and CGKP2DJZ6JSTBT1YXVEYDO2L53RKW2K0
# Sun, 25 Sep 2016 23:12:47: Done!
# Required 24.8965921402 seconds
# 
# real	0m24.954s
# user	0m19.112s
# sys	0m5.824s
