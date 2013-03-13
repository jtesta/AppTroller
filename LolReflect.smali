.class public Lcom/apptroller/LolReflect;
.super Ljava/lang/Object;
.source "LolReflect.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 16
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static varargs invoke(Ljava/lang/reflect/Method;Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;
    .locals 9
    .parameter "method"
    .parameter "receiver"
    .parameter "args"
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/lang/IllegalAccessException;,
            Ljava/lang/IllegalArgumentException;,
            Ljava/lang/reflect/InvocationTargetException;
        }
    .end annotation

    .prologue
    const/4 v8, 0x3

    const/4 v7, 0x2

    const/4 v6, 0x1

    const/4 v5, 0x0

    .line 19
    invoke-virtual {p0}, Ljava/lang/reflect/Method;->getName()Ljava/lang/String;

    move-result-object v0

    .line 20
    .local v0, methodName:Ljava/lang/String;
    const-string v2, "LolReflect"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "Method: "

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 21
    instance-of v2, p1, Landroid/accounts/AccountManager;

    if-eqz v2, :cond_0

    const-string v2, "getAccounts"

    invoke-virtual {v0, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_0

    .line 22
    invoke-static {}, Lcom/apptroller/LolAccount;->getAccounts()[Landroid/accounts/Account;

    move-result-object v1

    .line 38
    :goto_0
    return-object v1

    .line 23
    :cond_0
    instance-of v2, p1, Landroid/accounts/AccountManager;

    if-eqz v2, :cond_1

    const-string v2, "getAccountsByType"

    invoke-virtual {v0, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_1

    .line 24
    const-string v2, "LolReflect"

    const-string v3, "Trolled!"

    invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 25
    aget-object v2, p2, v5

    check-cast v2, Ljava/lang/String;

    invoke-static {v2}, Lcom/apptroller/LolAccount;->getAccountsByType(Ljava/lang/String;)[Landroid/accounts/Account;

    move-result-object v1

    goto :goto_0

    .line 26
    :cond_1
    instance-of v2, p1, Landroid/accounts/AccountManager;

    if-eqz v2, :cond_2

    const-string v2, "hasFeatures"

    invoke-virtual {v0, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_2

    .line 27
    aget-object v2, p2, v5

    check-cast v2, Landroid/accounts/Account;

    aget-object v3, p2, v6

    check-cast v3, [Ljava/lang/String;

    aget-object v4, p2, v7

    check-cast v4, Landroid/accounts/AccountManagerCallback;

    aget-object v5, p2, v8

    check-cast v5, Landroid/os/Handler;

    invoke-static {v2, v3, v4, v5}, Lcom/apptroller/LolAccount;->hasFeatures(Landroid/accounts/Account;[Ljava/lang/String;Landroid/accounts/AccountManagerCallback;Landroid/os/Handler;)Landroid/accounts/AccountManagerFuture;

    move-result-object v1

    goto :goto_0

    .line 28
    :cond_2
    instance-of v2, p1, Landroid/accounts/AccountManager;

    if-eqz v2, :cond_3

    const-string v2, "getAccountsByTypeAndFeatures"

    invoke-virtual {v0, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_3

    .line 29
    aget-object v2, p2, v5

    check-cast v2, Ljava/lang/String;

    aget-object v3, p2, v6

    check-cast v3, [Ljava/lang/String;

    aget-object v4, p2, v7

    check-cast v4, Landroid/accounts/AccountManagerCallback;

    aget-object v5, p2, v8

    check-cast v5, Landroid/os/Handler;

    invoke-static {v2, v3, v4, v5}, Lcom/apptroller/LolAccount;->getAccountsByTypeAndFeatures(Ljava/lang/String;[Ljava/lang/String;Landroid/accounts/AccountManagerCallback;Landroid/os/Handler;)Landroid/accounts/AccountManagerFuture;

    move-result-object v1

    goto :goto_0

    .line 31
    :cond_3
    const-string v2, "LolReflect"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "Not trollin: "

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {p1}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, "."

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    .line 32
    const/4 v1, 0x0

    .line 33
    .local v1, ret:Ljava/lang/Object;
    const-string v2, "hideApplicationBar"

    invoke-virtual {v0, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_4

    .line 34
    #const-string v2, "LolReflect"

    #const-string v3, "Found it!"

    #invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I
    invoke-virtual {p1}, Lcom/okcupid/okcupid/CommandHandler;->hideApplicationBar()V

    .line 37
    .end local v1           #ret:Ljava/lang/Object;
    :goto_1
    const-string v2, "LolReflect"

    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "Returning from invokation of "

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {v2, v3}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    goto/16 :goto_0

    .line 36
    .restart local v1       #ret:Ljava/lang/Object;
    :cond_4
    invoke-virtual {p0, p1, p2}, Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;

    move-result-object v1

    goto :goto_1
.end method
