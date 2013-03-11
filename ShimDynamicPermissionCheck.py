'''
ShimDynamicPermissionCheck.py
Copyright (C) 2012, Joe Testa <jtesta@positronsecurity.com>


This class shims android.app.Activity.checkCallingOrSelfPermission() calls.
'''

from FunctionCallParser import *
import os

class ShimDynamicPermissionCheck:

    @staticmethod
    def shim(codeDir, classPackage, lines, permissionCallIndex, neuteredPermissions):

        permissionCallString = lines[permissionCallIndex]
        fcp = FunctionCallParser(permissionCallString)

        # There seems to be a bug in apktool where a range-call (such as
        # 'invoke-virtual/range {v35 .. v36}, [...]') must be replaced with
        # another range-call (such as 'invoke-static/range {v35 .. v36}, [...]')
        newCall = 'invoke-static'
        varList = '{%s, %s}' % (fcp.object, fcp.args[0])
        if fcp.callType.endswith('/range'):
            newCall = 'invoke-static/range'
            varList = '{%s .. %s}' % (fcp.object, fcp.args[0])

        # If the original call was made on a Context, then we need to call
        # our checkOnContext() method.  Otherwise, the original call is on
        # an Activity.
        if fcp.functionClass == 'Landroid/content/Context':
            lines[permissionCallIndex] = "%s%s %s, L%s/LolPermissionChecker;->checkOnContext(Landroid/content/Context;Ljava/lang/String;)I\n" % (fcp.indentation, newCall, varList, classPackage)
        else:
            lines[permissionCallIndex] = "%s%s %s, L%s/LolPermissionChecker;->checkOnActivity(Landroid/app/Activity;Ljava/lang/String;)I\n" % (fcp.indentation, newCall, varList, classPackage)

        lolPermissionCheckPath = '%s/LolPermissionChecker.smali' % codeDir
        if not os.path.exists(lolPermissionCheckPath):
            hLolPermissionChecker = open(lolPermissionCheckPath, 'w')
            hLolPermissionChecker.write(""".class public final L%s/LolPermissionChecker;
.super Ljava/lang/Object;


.method public constructor <init>()V
    .locals 0

    .prologue
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method static checkOnActivity(Landroid/app/Activity;Ljava/lang/String;)I
    .locals 1

    .prologue
    invoke-virtual {p0}, Landroid/app/Activity;->getApplicationContext()Landroid/content/Context;

    move-result-object v0

    invoke-static {v0, p1}, L%s/LolPermissionChecker;->checkOnContext(Landroid/content/Context;Ljava/lang/String;)I

    move-result v0

    return v0
.end method

.method static checkOnContext(Landroid/content/Context;Ljava/lang/String;)I
    .locals 2

    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

""" % (classPackage, classPackage))

            for perm in neuteredPermissions:
                hLolPermissionChecker.write("""    const-string v1, "%s"\n\n""" % perm)
                hLolPermissionChecker.write("    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z\n\n")

            hLolPermissionChecker.write("""    invoke-virtual {v0, p1}, Ljava/util/ArrayList;->contains(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_0

    const/4 v0, 0x0

    :goto_0
    return v0

    :cond_0
    invoke-virtual {p0, p1}, Landroid/content/Context;->checkCallingOrSelfPermission(Ljava/lang/String;)I

    move-result v0

    goto :goto_0
.end method""")
            hLolPermissionChecker.close()
        return True
