.class public L[CLASSPATH]/LolAccount;
.super Ljava/lang/Object;
.source "LolAccount.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 8
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static getAccounts()[Landroid/accounts/Account;
    .locals 5

    .prologue
    .line 11
    const/4 v1, 0x1

    new-array v0, v1, [Landroid/accounts/Account;

    const/4 v1, 0x0

    new-instance v2, Landroid/accounts/Account;

    const-string v3, "[GOOGLEACCOUNT]"

    const-string v4, "com.google"

    invoke-direct {v2, v3, v4}, Landroid/accounts/Account;-><init>(Ljava/lang/String;Ljava/lang/String;)V

    aput-object v2, v0, v1

    .line 12
    .local v0, ret:[Landroid/accounts/Account;
    return-object v0
.end method

.method public static getAccountsByType(Ljava/lang/String;)[Landroid/accounts/Account;
    .locals 2
    .parameter "type"

    .prologue
    .line 16
    const-string v1, "com.google"

    invoke-virtual {p0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_0

    .line 17
    invoke-static {}, L[CLASSPATH]/LolAccount;->getAccounts()[Landroid/accounts/Account;

    move-result-object v0

    .line 20
    :goto_0
    return-object v0

    .line 19
    :cond_0
    const/4 v1, 0x0

    new-array v0, v1, [Landroid/accounts/Account;

    .line 20
    .local v0, ret:[Landroid/accounts/Account;
    goto :goto_0
.end method

.method public static getAccountsByTypeAndFeatures(Ljava/lang/String;[Ljava/lang/String;Landroid/accounts/AccountManagerCallback;Landroid/os/Handler;)Landroid/accounts/AccountManagerFuture;
    .locals 1
    .parameter "type"
    .parameter "features"
    .parameter
    .parameter "handler"
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            "[",
            "Ljava/lang/String;",
            "Landroid/accounts/AccountManagerCallback",
            "<[",
            "Landroid/accounts/Account;",
            ">;",
            "Landroid/os/Handler;",
            ")",
            "Landroid/accounts/AccountManagerFuture",
            "<[",
            "Landroid/accounts/Account;",
            ">;"
        }
    .end annotation

    .prologue
    .line 29
    .local p2, callback:Landroid/accounts/AccountManagerCallback;,"Landroid/accounts/AccountManagerCallback<[Landroid/accounts/Account;>;"
    new-instance v0, L[CLASSPATH]/LolAccountManagerFutureAccount;

    invoke-direct {v0, p0}, L[CLASSPATH]/LolAccountManagerFutureAccount;-><init>(Ljava/lang/String;)V

    return-object v0
.end method

.method public static hasFeatures(Landroid/accounts/Account;[Ljava/lang/String;Landroid/accounts/AccountManagerCallback;Landroid/os/Handler;)Landroid/accounts/AccountManagerFuture;
    .locals 1
    .parameter "account"
    .parameter "features"
    .parameter
    .parameter "handler"
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Landroid/accounts/Account;",
            "[",
            "Ljava/lang/String;",
            "Landroid/accounts/AccountManagerCallback",
            "<",
            "Ljava/lang/Boolean;",
            ">;",
            "Landroid/os/Handler;",
            ")",
            "Landroid/accounts/AccountManagerFuture",
            "<",
            "Ljava/lang/Boolean;",
            ">;"
        }
    .end annotation

    .prologue
    .line 25
    .local p2, callback:Landroid/accounts/AccountManagerCallback;,"Landroid/accounts/AccountManagerCallback<Ljava/lang/Boolean;>;"
    new-instance v0, L[CLASSPATH]/LolAccountManagerFutureBoolean;

    invoke-direct {v0}, L[CLASSPATH]/LolAccountManagerFutureBoolean;-><init>()V

    return-object v0
.end method
