'''
ShimExec.py
Copyright (C) 2012, Joe Testa <jtesta@positronsecurity.com>

This class shims java.lang.Runtime.exec() calls.
'''

from FunctionCallParser import *
import os

class ShimExec:

    @staticmethod
    def shim(codeDir, classPackage, lines, execIndex, readLogsStdout, readLogsStderr):
        #print "%s %s [%s] [%s] %d %d" % (codeDir, classPackage, lines[lastDotLocalsIndex], lines[execIndex], lastDotLocalsIndex, execIndex)


        fcp = FunctionCallParser(lines[execIndex])

        newExecCall = '%sinvoke-static {' % fcp.indentation
        for execArg in fcp.args:
            newExecCall = newExecCall + execArg + ', '
        newExecCall = newExecCall[:-2] + '}, L%s/LolExec;->exec(' % classPackage
        for execArgType in fcp.argTypes:
            newExecCall = newExecCall + execArgType + ';'
        newExecCall = newExecCall + ")Ljava/lang/Process;\n"

        lines[execIndex] = newExecCall

        # Write the LolExec class.  This checks to make sure that the program about to be
        # executed is not "logcat".  If it is, then a LolProcess is returned instead of a real
        # Process.  Otherwise, java.lang.Runtime.exec() is called with the original arguments.
        #
        # Note that LolExec has a lot of duplicated code.  This is for efficiency in execution
        # time.  This is disassembled code from the ShimCodeExec Android project code.
        lolExecPath = '%s/LolExec.smali' % codeDir
        if not os.path.exists(lolExecPath):
            hLolExec = open(lolExecPath, 'w')
            hLolExec.write(""".class public L%s/LolExec;
.super Ljava/lang/Object;


# direct methods
.method public constructor <init>()V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static exec(Ljava/lang/String;)Ljava/lang/Process;
    .locals 4
    #.parameter "prog"

    const/4 v3, 0x0

    const-string v1, " "

    invoke-virtual {p0, v1}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v0

    .local v0, p:[Ljava/lang/String;
    const/4 v1, 0x0

    aget-object v1, v0, v1

    invoke-virtual {v1}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v1

    const-string v2, "logcat"

    invoke-virtual {v1, v2}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_0

    new-instance v1, L%s/LolProcess;

    invoke-direct {v1}, L%s/LolProcess;-><init>()V

    :goto_0
    return-object v1

    :cond_0
    invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;

    move-result-object v1

    invoke-virtual {v1, p0, v3, v3}, Ljava/lang/Runtime;->exec(Ljava/lang/String;[Ljava/lang/String;Ljava/io/File;)Ljava/lang/Process;

    move-result-object v1

    goto :goto_0
.end method

.method public static exec(Ljava/lang/String;[Ljava/lang/String;)Ljava/lang/Process;
    .locals 3
    #.parameter "prog"
    #.parameter "envp"

    const-string v1, " "

    invoke-virtual {p0, v1}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v0

    .local v0, p:[Ljava/lang/String;
    const/4 v1, 0x0

    aget-object v1, v0, v1

    invoke-virtual {v1}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v1

    const-string v2, "logcat"

    invoke-virtual {v1, v2}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_0

    new-instance v1, L%s/LolProcess;

    invoke-direct {v1}, L%s/LolProcess;-><init>()V

    :goto_0
    return-object v1

    :cond_0
    invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;

    move-result-object v1

    const/4 v2, 0x0

    invoke-virtual {v1, p0, p1, v2}, Ljava/lang/Runtime;->exec(Ljava/lang/String;[Ljava/lang/String;Ljava/io/File;)Ljava/lang/Process;

    move-result-object v1

    goto :goto_0
.end method

.method public static exec(Ljava/lang/String;[Ljava/lang/String;Ljava/io/File;)Ljava/lang/Process;
    .locals 3
    #.parameter "prog"
    #.parameter "envp"
    #.parameter "directory"

    const-string v1, " "

    invoke-virtual {p0, v1}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v0

    .local v0, p:[Ljava/lang/String;
    const/4 v1, 0x0

    aget-object v1, v0, v1

    invoke-virtual {v1}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v1

    const-string v2, "logcat"

    invoke-virtual {v1, v2}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_0

    new-instance v1, L%s/LolProcess;

    invoke-direct {v1}, L%s/LolProcess;-><init>()V

    :goto_0
    return-object v1

    :cond_0
    invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;

    move-result-object v1

    invoke-virtual {v1, p0, p1, p2}, Ljava/lang/Runtime;->exec(Ljava/lang/String;[Ljava/lang/String;Ljava/io/File;)Ljava/lang/Process;

    move-result-object v1

    goto :goto_0
.end method

.method public static exec([Ljava/lang/String;)Ljava/lang/Process;
    .locals 3
    #.parameter "progArray"

    const/4 v2, 0x0

    const/4 v0, 0x0

    aget-object v0, p0, v0

    invoke-virtual {v0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    const-string v1, "logcat"

    invoke-virtual {v0, v1}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_0

    new-instance v0, L%s/LolProcess;

    invoke-direct {v0}, L%s/LolProcess;-><init>()V

    :goto_0
    return-object v0

    :cond_0
    invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;

    move-result-object v0

    invoke-virtual {v0, p0, v2, v2}, Ljava/lang/Runtime;->exec([Ljava/lang/String;[Ljava/lang/String;Ljava/io/File;)Ljava/lang/Process;

    move-result-object v0

    goto :goto_0
.end method

.method public static exec([Ljava/lang/String;[Ljava/lang/String;)Ljava/lang/Process;
    .locals 2
    #.parameter "progArray"
    #.parameter "envp"

    const/4 v0, 0x0

    aget-object v0, p0, v0

    invoke-virtual {v0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    const-string v1, "logcat"

    invoke-virtual {v0, v1}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_0

    new-instance v0, L%s/LolProcess;

    invoke-direct {v0}, L%s/LolProcess;-><init>()V

    :goto_0
    return-object v0

    :cond_0
    invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;

    move-result-object v0

    const/4 v1, 0x0

    invoke-virtual {v0, p0, p1, v1}, Ljava/lang/Runtime;->exec([Ljava/lang/String;[Ljava/lang/String;Ljava/io/File;)Ljava/lang/Process;

    move-result-object v0

    goto :goto_0
.end method

.method public static exec([Ljava/lang/String;[Ljava/lang/String;Ljava/io/File;)Ljava/lang/Process;
    .locals 2
    #.parameter "progArray"
    #.parameter "envp"
    #.parameter "directory"

    const/4 v0, 0x0

    aget-object v0, p0, v0

    invoke-virtual {v0}, Ljava/lang/String;->trim()Ljava/lang/String;

    move-result-object v0

    const-string v1, "logcat"

    invoke-virtual {v0, v1}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_0

    new-instance v0, L%s/LolProcess;

    invoke-direct {v0}, L%s/LolProcess;-><init>()V

    :goto_0
    return-object v0

    :cond_0
    invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;

    move-result-object v0

    invoke-virtual {v0, p0, p1, p2}, Ljava/lang/Runtime;->exec([Ljava/lang/String;[Ljava/lang/String;Ljava/io/File;)Ljava/lang/Process;

    move-result-object v0

    goto :goto_0
.end method""" % (classPackage, classPackage, classPackage, classPackage, classPackage, classPackage, classPackage, classPackage, classPackage, classPackage, classPackage, classPackage, classPackage))
            hLolExec.close()

        lolProcessPath = '%s/LolProcess.smali' % codeDir
        if not os.path.exists(lolProcessPath):
            hLolProcess = open(lolProcessPath, 'w')
            hLolProcess.write(""".class public final L%s/LolProcess;
.super Ljava/lang/Process;

.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Ljava/lang/Process;-><init>()V
    return-void
.end method

.method public final destroy()V
    .locals 0
    return-void
.end method

.method public final exitValue()I
    .locals 1
    const/4 v0, 0x0
    return v0
.end method

.method public final getErrorStream()Ljava/io/InputStream;
    .locals 2
    new-instance v0, Ljava/io/ByteArrayInputStream;
    const-string v1, "%s"
    invoke-virtual {v1}, Ljava/lang/String;->getBytes()[B
    move-result-object v1
    invoke-direct {v0, v1}, Ljava/io/ByteArrayInputStream;-><init>([B)V
    return-object v0
.end method

.method public final getInputStream()Ljava/io/InputStream;
    .locals 2
    new-instance v0, Ljava/io/ByteArrayInputStream;
    const-string v1, "%s"
    invoke-virtual {v1}, Ljava/lang/String;->getBytes()[B
    move-result-object v1
    invoke-direct {v0, v1}, Ljava/io/ByteArrayInputStream;-><init>([B)V
    return-object v0
.end method

.method public final getOutputStream()Ljava/io/OutputStream;
    .locals 1
    new-instance v0, L%s/LolOutputStream;
    invoke-direct {v0}, L%s/LolOutputStream;-><init>()V
    return-object v0
.end method

.method public final waitFor()I
    .locals 1
    const/4 v0, 0x0
    return v0
.end method
""" % (classPackage, readLogsStderr, readLogsStdout, classPackage, classPackage))
            hLolProcess.close()

        lolOutputStreamPath = '%s/LolOutputStream.smali' % codeDir
        if not os.path.exists(lolOutputStreamPath):
            hLolOutputStream = open(lolOutputStreamPath, 'w')
            hLolOutputStream.write(""".class public final L%s/LolOutputStream;
.super Ljava/io/OutputStream;

.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Ljava/io/OutputStream;-><init>()V
    return-void
.end method

.method public final close()V
    .locals 0
    return-void
.end method

.method public final flush()V
    .locals 0
    return-void
.end method

.method public final write(I)V
    .locals 0
    return-void
.end method

.method public final write([B)V
    .locals 0
    return-void
.end method

.method public final write([BII)V
    .locals 0
    return-void
.end method
""" % classPackage)
            hLolOutputStream.close()

        # Return freeGotoIndex, nextFreeVar, modifiedBoolean
        return True
