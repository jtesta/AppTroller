'''
PostProcessor.py
Copyright (C) 2012, Joe Testa <jtesta@positronsecurity.com>

This class performs post-processing (last-minute) tasks on disassembled
sources.  Currently, this only looks for empty try-catch blocks and removes
the catch lines (otherwise Dalvik crashes).
'''

from CatchBlockParser import *
class PostProcessor:

    # We take an array of code lines and possibly modify it.
    def process(self, lines):

        # Loop through all the lines.
        labels = {}
        i = 0
        while i < len(lines):
            line = lines[ i ].strip()

            # Labels (i.e.: ":try_start_0") are unique to each method.  So
            # we reset our dictionary of labels when we encounter a new method.
            if line.startswith('.method'):
                labels = {}

            # When we find a label, store its line number.
            if line.startswith(':'):
                labels[line] = i

            # Parse all catch blocks.
            if line.startswith('.catch'):
                cbp = CatchBlockParser(line)

                # Get the labels that denote the start and end of the try block.
                startLabel = cbp.startLabel
                endLabel = cbp.endLabel

                # Get the line number of the start label.
                startLabelPos = labels[startLabel]

                # Loop from the start label until either the end label is found
                # or we find a non-empty line.
                endLabelNotFound = True
                blockIsEmpty = True
                j = startLabelPos + 1
                while endLabelNotFound and blockIsEmpty:
                    templine = lines[ j ].strip()
                    if templine == endLabel:
                        endLabelNotFound = False
                    elif templine != '':
                        blockIsEmpty = False
                    else:
                        j = j + 1
            
                # If this try-catch block is empty, we remove the catchb line
                # so Dalvik doesn't crash.
                if blockIsEmpty:
                    lines[ i ] = ''

            i = i + 1
