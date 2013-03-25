'''
ShimGetAccounts.py
Copyright (C) 2013, Joe Testa <jtesta@positronsecurity.com>


This class shims calls for the GET_ACCOUNT permission.
'''

from FunctionCallParser import *
import os


class ShimGetAccounts:

    @staticmethod
    def shim(codeDir, classPackage, lines, lineIndex, googleAccount):

        code = lines[lineIndex]
        fcp = FunctionCallParser(code)

        # There seems to be a bug in apktool where a range-call (such as
        # 'invoke-virtual/range {v35 .. v36}, [...]') must be replaced with
        # another range-call (such as 'invoke-static/range {v35 .. v36}, [...]')
        newCall = 'invoke-static'
        varList = '{%s}' % ', '.join(fcp.args)
        if fcp.callType.endswith('/range'):
            newCall = 'invoke-static/range'
            varList = '{%s .. %s}' % (fcp.args[0], fcp.args[len(fcp.args) - 1])


        if fcp.method == 'getAccounts':
            lines[lineIndex] = '%sinvoke-static {}, L%s/LolAccount;->getAccounts()[Landroid/accounts/Account;\n' % (fcp.indentation, classPackage)
        elif fcp.method == 'getAccountsByType':
            lines[lineIndex] = '%sinvoke-static {%s}, L%s/LolAccount;->getAccountsByType(Ljava/lang/String;)[Landroid/accounts/Account;\n' % (fcp.indentation, fcp.args[0], classPackage)
        elif fcp.method == 'getAccountsByTypeAndFeatures':
            lines[lineIndex] = '%s%s %s, L%s/LolAccount;->getAccountsByTypeAndFeatures(Ljava/lang/String;[Ljava/lang/String;Landroid/accounts/AccountManagerCallback;Landroid/os/Handler;)Landroid/accounts/AccountManagerFuture;\n' % (fcp.indentation, newCall, varList, classPackage)
        elif fcp.method == 'hasFeatures':
            lines[lineIndex] = '%s%s %s, L%s/LolAccount;->hasFeatures(Landroid/accounts/Account;[Ljava/lang/String;Landroid/accounts/AccountManagerCallback;Landroid/os/Handler;)Landroid/accounts/AccountManagerFuture;\n' % (fcp.indentation, newCall, varList, classPackage)

        ShimGetAccounts.writeCode(codeDir, classPackage, googleAccount)
        return True


    @staticmethod
    def writeCode(codeDir, classPackage, googleAccount):

        lolAccountPath = '%s/LolAccount.smali' % codeDir
        if not os.path.exists(lolAccountPath):
            hSmaliCode = open('smali/ShimGetAccounts_LolAccount.smali', 'r')
            smaliCode = hSmaliCode.read()
            hSmaliCode.close()

            smaliCode = smaliCode.replace('[CLASSPATH]', classPackage)
            smaliCode = smaliCode.replace('[GOOGLEACCOUNT]', googleAccount)

            hLolAccounts = open(lolAccountPath, 'w')
            hLolAccounts.write(smaliCode)
            hLolAccounts.close()


        lolAccountPath = '%s/LolAccountManagerFutureBoolean.smali' % codeDir
        if not os.path.exists(lolAccountPath):
            hSmaliCode = open('smali/ShimGetAccounts_LolAccountManagerFutureBoolean.smali', 'r')
            smaliCode = hSmaliCode.read()
            hSmaliCode.close()

            smaliCode = smaliCode.replace('[CLASSPATH]', classPackage)

            hLolAccounts = open(lolAccountPath, 'w')
            hLolAccounts.write(smaliCode)
            hLolAccounts.close()


        lolAccountPath = '%s/LolAccountManagerFutureAccount.smali' % codeDir
        if not os.path.exists(lolAccountPath):
            hSmaliCode = open('smali/ShimGetAccounts_LolAccountManagerFutureAccount.smali', 'r')
            smaliCode = hSmaliCode.read()
            hSmaliCode.close()

            smaliCode = smaliCode.replace('[CLASSPATH]', classPackage)

            hLolAccounts = open(lolAccountPath, 'w')
            hLolAccounts.write(smaliCode)
            hLolAccounts.close()

        return
