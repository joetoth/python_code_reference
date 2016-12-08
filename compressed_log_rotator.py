#!/usr/bin/env python

# Import all the needed modules
import logging.handlers
import sys
import time
import gzip
import os
import shutil
import random
import string

__author__ = "Rakesh Challagonda (rkreddy46@gmail.com)"
__version__ = 1.0
__descr__ = "This logic is written keeping in mind UNIX/LINUX/OSX platforms only"


# Create a new class that inherits from RotatingFileHandler. This is where we add the new feature to compress the logs
class CompressedRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = "%s.%d.gz" % (self.baseFilename, i)
                dfn = "%s.%d.gz" % (self.baseFilename, i + 1)
                if os.path.exists(sfn):
                    # print "%s -> %s" % (sfn, dfn)
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.baseFilename + ".1.gz"
            if os.path.exists(dfn):
                os.remove(dfn)
            # These two lines below are the only new lines. I commented out the os.rename(self.baseFilename, dfn) and
            #  replaced it with these two lines.
            with open(self.baseFilename, 'rb') as f_in, gzip.open(dfn, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            # os.rename(self.baseFilename, dfn)
            # print "%s -> %s" % (self.baseFilename, dfn)
        self.mode = 'w'
        self.stream = self._open()

# Specify which file will be used for our logs
log_filename = "/Users/rakesh.challagonda/Downloads/test_logs/sample_log.txt"

# Create a logger instance and set the facility level
my_logger = logging.getLogger()
my_logger.setLevel(logging.DEBUG)

# Create a handler using our new class that rotates and compresses
file_handler = CompressedRotatingFileHandler(filename=log_filename, maxBytes=1000000, backupCount=10)

# Create a stream handler that shows the same log on the terminal (just for debug purposes)
view_handler = logging.StreamHandler(stream=sys.stdout)

# Add all the handlers to the logging instance
my_logger.addHandler(file_handler)
my_logger.addHandler(view_handler)

# This is optional to beef up the logs
random_huge_data = "".join(random.choice(string.ascii_letters) for _ in xrange(10000))

# All this code is user-specific, write your own code if you want to play around
count = 0
while True:
    my_logger.debug("This is the message number %s" % str(count))
    my_logger.debug(random_huge_data)
    count += 1
    if count % 100 == 0:
        count = 0
        time.sleep(2)
