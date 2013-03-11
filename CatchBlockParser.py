'''
CatchBlockParser.py
Copyright (C) 2012, Joe Testa <jtesta@positronsecurity.com>

This class parses the ".catch" code lines and parses out the exception class
caught, along with the start, end, and catch labels.
'''

import re

class CatchBlockParser:

    def __init__(self, catchString):
        catchString = catchString.strip()
        #self.catchString = catchString

        if (not catchString.startswith('.catch')):
            raise Exception, 'This is not a catch block!: %s' % catchString

        # Example:
        # .catch Ljava/lang/SecurityException; {:try_start_0 .. :try_end_0} :catch_0
        re1 = re.compile(r'.catch (.*?) {(.*?) .. (.*?)} (.*)')
        m = re1.match(catchString)
        if m:
            self.exceptionClass = m.group(1)[1:-1]
            self.startLabel = m.group(2)
            self.endLabel = m.group(3)
            self.catchLabel =  m.group(4)
        else:

            # Example:
            # .catchall {:try_start_0 .. :try_end_0} :catchall_0
            re1 = re.compile(r'.catchall {(.*?) .. (.*?)} (.*)')
            m = re1.match(catchString)
            if m:
                self.exceptionClass = '*'
                self.startLabel = m.group(1)
                self.endLabel = m.group(2)
                self.catchLabel = m.group(3)
            else:
                raise Exception, 'Could not match catch block structure on: %s' % catchString
