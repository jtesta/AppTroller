'''
ShimReflection.py
Copyright (C) 2013, Joe Testa <jtesta@positronsecurity.com>


This class shims calls for reflection.
'''

from FunctionCallParser import *
from ShimGetAccounts import *
import os, shutil


class ShimReflection:

    @staticmethod
    def shim(codeDir, classPackage, lines, lineIndex, googleAccount):

        code = lines[lineIndex]
        fcp = FunctionCallParser(code)

        # There seems to be a bug in apktool where a range-call (such as
        # 'invoke-virtual/range {v35 .. v36}, [...]') must be replaced with
        # another range-call (such as 'invoke-static/range {v35 .. v36}, [...]')
        newCall = 'invoke-static'
        varList = '{%s, %s}' % (fcp.object, ', '.join(fcp.args))
        if fcp.callType.endswith('/range'):
            newCall = 'invoke-static/range'
            varList = '{%s .. %s}' % (fcp.object, fcp.args[len(fcp.args) - 1])

        lines[lineIndex] = '%s%s %s, L%s/LolReflect;->invoke(Ljava/lang/reflect/Method;%s;)%s;\n' % (fcp.indentation, newCall, varList, classPackage, ';'.join(fcp.argTypes), fcp.returnType)

        ShimGetAccounts.writeCode(codeDir, classPackage, googleAccount)
        ShimReflection.writeCode(codeDir)
        return True


    @staticmethod
    def writeCode(codeDir):
        destinationFile = '%s/LolReflect.smali' % codeDir
        if not os.path.exists(destinationFile):
            shutil.copyfile('smali/LolReflect.smali', destinationFile)
        return
