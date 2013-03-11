'''
ShimReadContacts.py
Copyright (C) 2013, Joe Testa <jtesta@positronsecurity.com>


This class shims android.content.ContentResolver.query() calls.

** This is EXPERIMENTAL! **
'''

from FunctionCallParser import *
import os


class ShimReadContacts:

    @staticmethod
    def shim(codeDir, classPackage, lines, queryCallIndex):

        queryCallString = lines[queryCallIndex]
        fcp = FunctionCallParser(queryCallString)

        # There seems to be a bug in apktool where a range-call (such as
        # 'invoke-virtual/range {v35 .. v36}, [...]') must be replaced with
        # another range-call (such as 'invoke-static/range {v35 .. v36}, [...]')
        newCall = 'invoke-static'
        varList = '{%s, %s}' % (fcp.object, ', '.join(fcp.args))
        if fcp.callType.endswith('/range'):
            newCall = 'invoke-static/range'
            varList = '{%s .. %s}' % (fcp.object, fcp.args[len(fcp.args) - 1])

        lines[queryCallIndex] = "%s%s %s, L%s/LolContacts;->query(Landroid/net/Uri;[Ljava/lang/String;Ljava/lang/String;[Ljava/lang/String;Ljava/lang/String;)Landroid/database/Cursor;\n" % (fcp.indentation, newCall, varList, classPackage)


        lolContactsPath = '%s/LolContacts.smali' % codeDir
        if not os.path.exists(lolContactsPath):
            hSmaliCode = open('ShimReadContacts.smali', 'r')
            smaliCode = hSmaliCode.read()
            hSmaliCode.close()

            smaliCode = smaliCode.replace('[CLASSPATH]', classPackage)

            hLolContacts = open(lolContactsPath, 'w')
            hLolContacts.write(smaliCode)
            hLolContacts.close()
        return True
