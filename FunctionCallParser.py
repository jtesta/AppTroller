'''
FunctionCallParser.py
Copyright (C) 2012, Joe Testa <jtesta@positronsecurity.com>


This class parses function calls so that the objects, arguments, and 
argument types can be extracted.  For example:

>>> from FunctionCallParser import *
>>> fcp = FunctionCallParser('    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V')
>>> print fcp.callType
direct
>>> print fcp.functionClass
Ljava/lang/StringBuilder
>>> print fcp.method
<init>
>>> print fcp.object
v3
>>> print fcp.args
['v4']
>>> print fcp.argTypes
['Ljava/lang/String']
>>> print fcp.returnType
V
>>> print '%sThis is indented four spaces.' % fcp.indentation
    This is indented four spaces.
'''

import re, string

class FunctionCallParser:

    def __init__(self, functionCallString):

        self.callType = None
        self.object = None
        self.functionClass = None
        self.method = None
        self.args = []
        self.argTypes = []

        charNotFound = True
        i = 0
        while charNotFound:
            if functionCallString[ i ] == ' ':
                i = i + 1
            else:
                charNotFound = False

        self.indentation = functionCallString[:i]

        re1 = re.compile(r'invoke-(.*?) {(.*?)}, (.*?)->(.*?)\((.*?)\)(.*)')
        m = re1.match(functionCallString.strip())
        if m:
            # For an input of "invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V", callType will be "direct" and variables will be "v3, v4"
            self.callType = m.group(1)
            variables = m.group(2)
            self.functionClass = m.group(3)[:-1]
            self.method = m.group(4)

            # -1 cuts off the last semicolon
            self.argTypes = m.group(5)[:-1].split(';') 

            self.returnType = m.group(6)
            if self.returnType.endswith(';'):
                self.returnType = self.returnType[:-1]

            # If the call type is a range, then the variables are in the format
            # of something like "{v2 .. v7}", so we must expand this into a
            # list such
            # as ['v3', 'v4', 'v5', 'v6', 'v7'].
            if self.callType.find('/range') != -1:

                # Extract the endpoints.
                varEndpoints = re.compile(r'^(.+?) .. (.+?)$')
                m = varEndpoints.match(variables)
                if m:
                    # From an endpoint of "v2", extract the integer.
                    varStart = int(m.group(1)[1:])
                    varEnd = int(m.group(2)[1:])

                    # Hold onto the prefix ("v").
                    varPrefix = m.group(1)[0:1]
                
                    # Iterate between the endpoints to create the list.  We
                    # start with the first variable +1 because the second
                    # variable is actually the first argument (i.e.: its
                    # actually something like v2.function(v3, v4, v5), etc).
                    self.object = "%s%d" % (varPrefix, varStart)
                    n = varStart + 1
                    while (n <= varEnd):
                        self.args.append("%s%d" % (varPrefix, n))
                        n = n + 1

                else:  # If we can't parse the input, barf.
                    raise Exception, 'Could not parse function call string: %s' % functionCallString

            else:
                # If all the variables are explicitly listed ("v2, v3, v4"),
                # then we can just split the string by ", " into a list, and 
                # skip the first entry (see above).
                varArray = string.split(variables, ', ')
                self.object = varArray[0]
                self.args = varArray[1:]

        else:  # If we can't parse the input, barf.
            raise Exception, 'Could not parse function call string: %s' % functionCallString
