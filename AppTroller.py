'''
AppTroller.py
Copyright (C) 2012, 2013 Joe Testa <jtesta@positronsecurity.com>

This script trolls Android apps.  Hard.

'''

import getopt, hashlib, os, random, re, shutil, string, struct, subprocess, sys, tarfile, tempfile, urllib2
from PostProcessor import *
from ShimDynamicPermissionCheck import *
from ShimExec import *
from ShimReadContacts import *
from ShimGetAccounts import *
from ShimReflection import *


APPTROLLER_VERSION = '0.03'
APPTROLLER_DATE = 'January 3, 2013'

APKTOOL_URL = 'https://android-apktool.googlecode.com/files/apktool1.5.2.tar.bz2'
APKTOOL_HASH = '2dd828cf79467730c7406aa918f1da1bd21aaec8'


neuteredPermissions = []
functionToValueMap = {}
functionShimMap = {}


# Sends an error message to stderr.  If the 'term' argument is True, terminate
# the program.
def e(msg, term):
    print >> sys.stderr, 'Error: %s' % msg
    if term:
        sys.exit(1)


# Sends a debugging message to stdout if the debugging flag is set.
def d(msg):
    if debug:
        print msg


# Sends a verbose message to stdout if the verbose flag is set.
def v(msg):
    if verbose:
        print msg


# Downloads apktool.jar and places it in the current directory.  Terminates
# on error.
def getAPKTool():
    print 'Downloading apktool...'

    # Note that while the URL is HTTPS, urllib2 does not check the server's
    # certificate, so its effectively the same as HTTP.  We will verify the
    # archive hash manually below...
    hArchive = urllib2.urlopen(APKTOOL_URL)
    archive = hArchive.read()
    hArchive.close()

    # Calculate the SHA1 sum of the archive so we can compare it with the
    # expected value.
    h = hashlib.sha1()
    h.update(archive)

    archiveHash = h.hexdigest()
    print "Done.  Downloaded SHA1 hash is %s. " % archiveHash
    if archiveHash != APKTOOL_HASH:
        e('Hash does not correspond to expected value (%s).  Terminating.' % APKTOOL_HASH, True)

    # Create a temporary directory securely for us to extract the archive to.
    tempDir = tempfile.mkdtemp()
    tempTarFile = tempDir + '/apktool.tar.bz2'
    print 'Hash value is verified.  Writing archive to %s...' % tempTarFile
    hTarFile = open(tempTarFile, 'w')
    hTarFile.write(archive)
    hTarFile.close()
    archive = None

    # Open the archive and look at the entries inside before compressing.  Make
    # sure that they won't end up writing files outside the target directory
    # using relative paths.
    hTarFile = tarfile.open(tempTarFile, 'r:bz2')
    tarFileIsBad = False
    for entry in hTarFile.getnames():
        if entry.startswith('/') or entry.find('..') != -1:
            tarFileIsBad = True

    if tarFileIsBad:
        hTarFile.close()
        shutil.rmtree(tempDir)
        e('The downloaded apktool archive has dangerous path names in it!  Terminating without extracting.', True)

    # Extract all the entries in the archive.
    print 'Extracting archive to temporary directory...'
    hTarFile.extractall(tempDir)
    hTarFile.close()

    # Look for the jar file.  There should only be one.
    jarPath = None
    for root, directory, files in os.walk(tempDir):
        for f in files:
            if f.endswith('.jar'):
                jarPath = root + '/' + f

    if jarPath is None:
        e('Could not find jar file in archive.  Terminating.', True)

    # Move the jar file to apktool.jar in the current directory.
    print 'Moving apktool.jar to current directory...'
    shutil.move(jarPath, 'apktool.jar')

    # Recursively delete the temporary directory.
    print 'Deleting temporary directory %s...' % tempDir
    shutil.rmtree(tempDir)

    print "\nDone!  apktool.jar downloaded successfully.\n"


def makeAllMethodsPublic(filesWithUnhandledMethods):
    for smaliPath in filesWithUnhandledMethods:
        d('Re-processing %s...' % smaliPath)

        hSmali = open(smaliPath, 'r')
        lines = hSmali.readlines()
        hSmali.close()

        modified = False
        i = 0
        while i < len(lines):
            line = lines[ i ]
            sline = line.strip()
            if sline.startswith('.method') and sline.find('<init>') == -1 and line.find('<clinit>') == -1:
                tokens = sline.split()
                if tokens[1] == 'protected' or tokens[1] == 'private':
                    tokens[1] = 'public'
                    modified = True
                elif tokens[1] != 'public':
                    tokens.insert(1, 'public')
                    modified = True

                lines[ i ] = ' '.join(tokens) + "\n"

            if sline.startswith('invoke-'):
                idPos = line.find('invoke-direct')
                if idPos != -1 and line.find('<init>') == -1 and line.find('<clinit>') == -1:
                    line = line[:idPos] + 'invoke-virtual' + line[idPos + 13:]
                    lines[ i ] = line
                    modified = True


            i = i + 1


        if modified:
            d('    Modified: %s' % smaliPath)
            hSmali = open(smaliPath, 'w')
            hSmali.write(''.join(lines))
            hSmali.close()



#def checkKeyStore():
def makeKeyStore(path):
    #if not os.path.exists('umadbro.keystore'):
    #print 'Keystore not found.  Generating...'
    v('Generating keystore... ',)

    stdDestination = subprocess.PIPE
    if verbose:
        stdDestination = None

    p = subprocess.Popen(['keytool', '-genkey', '-keystore', path, '-alias', 'lol', '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000', '-storepass', 'abcdef'], stdin=subprocess.PIPE, stdout=stdDestination, stderr=stdDestination, close_fds=True)
    p.communicate("Mike Hunt\nu mad bro?\nlol\nRochester\nNY\nUS\nyes\n\n")
    p.wait()
    #print 'Done.'
    v("\nDone generating keystore.")


def escapeStr(stuff):
    return stuff.replace("'", "\\'").replace('"', '\\"')


def usage(exitval):
    print
    print
    print 'AppTroller v%s (%s)' % (APPTROLLER_VERSION, APPTROLLER_DATE)
    print
    print 'Usage:  python AppTroller.py [OPTIONS] input.apk output.apk'
    print
    print
    print "  -c, --config       Specify an alternate configuration file (default is\n                           'troll.cfg'."
    print "  -d, --debug        Enable debugging mode (implies verbose mode)."
    print "  -k, --keep         Keep the disassembled sources instead of deleting them\n                           when finished."
    print "  -K, --Keep         Keep the diff file only (a dest. path be specified)."
    print "  -v, --verbose      Enable verbose mode."
    print
    print
    sys.exit(exitval)


# Check that the programs we need are available.
missingTools = []
if os.system('java -jar apktool.jar > /dev/null 2> /dev/null') == 256:
    print 'apktool.jar was not found.  Download it? [Y/n]:',
    yOrN = raw_input()
    if yOrN == '' or yOrN.lower() == 'y':
        getAPKTool()
    else:
        e('apktool.jar was not found, and you chose not to get it.  Download it manually at <https://code.google.com/p/android-apktool/downloads/list> and place apktool.jar in this directory.', True)
if os.system('keytool -help > /dev/null 2> /dev/null') != 256:
    missingTools.append('keytool')
if os.system('diff -v > /dev/null 2> /dev/null') != 0:
    missingTools.append('diff')
if os.system('jarsigner > /dev/null 2> /dev/null') != 256:
    missingTools.append('jarsigner')
if os.system('zipalign > /dev/null 2> /dev/null') != 512:
    missingTools.append('zipalign')

# If anything is missing, print out the list and halt.
if len(missingTools) > 0:
    e("the following tools are missing from your path:\n\t%s\n" % "\n\t".join(missingTools), True)


opts = None
args = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "c:K:dhkv", ["config=", "Keep=", "debug", "help", "keep", "verbose"])
except getopt.GetoptError, err:
    print
    e('%s' % str(err), False)
    usage(1)


configFile = 'troll.cfg'
keepFlag = False
keepDiff = None
debug = False
verbose = False
for o, a in opts:
    if o in ('-c', '--config'):
        configFile = a
    elif o in ('-d', '--debug'):
        # Debug mode implies verbose mode.
        debug = True
        verbose = True
    elif o in ('-k', '--keep'):
        keepFlag = True
    elif o in ('-K', '--Keep'):
        keepDiff = a
    elif o in ('-h', '--help'):
        usage(0)
    elif o in ('-v', '--verbose'):
        verbose = True

if len(args) == 0:
    usage(1)

if keepFlag and (keepDiff is not None):
    e('-k/--keep and -K/--Keep cannot be used together!', True)

# Yes, even though the user can't specify both, we set this flag anyway so that
# a diff file is made.  Then we'll switch it off later...
if keepDiff is not None:
    keepFlag = True

if keepDiff == '':
    e('-K/--Keep must specify a specific destination path for the diff file.', True)

originalAPK = args[0]
outputAPK = args[1]


if not os.path.exists(originalAPK):
    e('Original APK not found: %s' % originalAPK, True)


hConfig = open(configFile, 'r')
if not hConfig:
    e('could not open %s!' % configFile, True)

read_phone_state = False
send_sms = False
receive_sms = False
system_alert_window = False
read_logs = False
line_number = ''
device_id = ''
device_software_version = ''
sim_serial_number = ''
subscriber_id = ''
voicemail_alpha_tag = ''
voicemail_number = ''
dynamicPermissionCheck = False
read_contacts = False
write_contacts = False
get_accounts = False
googleAccount = ''
enableDebug = False
for line in hConfig:
    line = line.strip()
    if (line is not '') and (not line.startswith('#')):
        tokens = line.split('=')
        key = tokens[0].strip().lower()
        value = tokens[1].strip()
        lvalue = value.lower()
        if key == 'read_phone_state' and lvalue == 'enabled':
            read_phone_state = True
            neuteredPermissions.append('android.permission.READ_PHONE_STATE')
        elif key == 'line_number':
            line_number = escapeStr(value)
        elif key == 'device_id':
            device_id = escapeStr(value)
        elif key == 'device_software_version':
            device_software_version = escapeStr(value)
        elif key == 'sim_serial_number':
            sim_serial_number = escapeStr(value)
        elif key == 'subscriber_id':
            subscriber_id = escapeStr(value)
        elif key == 'voicemail_alpha_tag':
            voicemail_alpha_tag = escapeStr(value)
        elif key == 'voicemail_number':
            voicemail_number = escapeStr(value)
        elif key == 'send_sms' and lvalue == 'enabled':
            send_sms = True
            neuteredPermissions.append('android.permission.SEND_SMS')
        elif key == 'receive_sms' and lvalue == 'enabled':
            receive_sms = True
            neuteredPermissions.append('android.permission.RECEIVE_SMS')
        elif key == 'system_alert_window' and lvalue == 'enabled':
            system_alert_window = True
            neuteredPermissions.append('android.permission.SYSTEM_ALERT_WINDOW')
        elif key == 'read_logs' and lvalue == 'enabled':
            read_logs = True
            neuteredPermissions.append('android.permission.READ_LOGS')
        elif key == 'read_logs_stdout':
            readLogsStdout = escapeStr(value)
        elif key == 'read_logs_stderr':
            readLogsStderr = escapeStr(value)
        elif key == 'dynamic_permission_check' and lvalue == 'enabled':
            dynamicPermissionCheck = True
        elif key == 'read_contacts' and lvalue == 'enabled':
            read_contacts = True
            write_contacts = True  # This is also set for safety.  Breaks stuff though.
            neuteredPermissions.append('android.permission.READ_CONTACTS')
            neuteredPermissions.append('android.permission.WRITE_CONTACTS')
        elif key == 'get_accounts' and lvalue == 'enabled':
            get_accounts = True
            neuteredPermissions.append('android.permission.GET_ACCOUNTS')
        elif key == 'google_account':
            googleAccount = escapeStr(value)
        elif key == 'enable_debug':
            enableDebug = True


hConfig.close()


# Pad the line_number until we have at least 11 digits.  We're too good to use
# the standard rand() function.... because hey... what if someone uses our
# phone number as cryptographic key material?  :P
while len(line_number) < 11:
    bytes = os.urandom(8)
    line_number = line_number + str(struct.unpack('BBBBBBBB', bytes)[0])

# If the number is too big, trim it so its exactly 11 digits.
if len(line_number) > 11:
    line_number = line_number[:11]

# If the device_id is not set, we will generate a random 15 digit IMSI-looking
# value.
if device_id == '':
    while len(device_id) < 15:
        bytes = os.urandom(8)
        device_id = device_id + str(struct.unpack('BBBBBBBB', bytes)[0])
    if len(device_id) > 15:
        device_id = device_id[:15]

if device_software_version == '':
    device_software_version = '0'

if sim_serial_number == '':
    while len(sim_serial_number) < 20:
        bytes = os.urandom(8)
        sim_serial_number = sim_serial_number + str(struct.unpack('BBBBBBBB', bytes)[0])
    if len(sim_serial_number) > 20:
        sim_serial_number = sim_serial_number[:20]

if subscriber_id == '':
    while len(subscriber_id) < 16:
        bytes = os.urandom(8)
        subscriber_id = subscriber_id + str(struct.unpack('BBBBBBBB', bytes)[0])
    if len(subscriber_id) > 16:
        subscriber_id = subscriber_id[:16]

if voicemail_alpha_tag == '':
    voicemail_alpha_tag = 'Voice Mail'

if voicemail_number == '':
    voicemail_number = '+' + line_number

if googleAccount == '':
    letters = ''.join(random.choice(string.ascii_lowercase) for x in range(8))
    numbers = ''.join(random.choice(string.digits) for x in range(3))
    googleAccount = '%s%s@gmail.com' % (letters, numbers)


# If we're supposed to neuter the READ_PHONE_STATE calls.
if read_phone_state:
    functionToValueMap['Landroid/telephony/TelephonyManager;->getDeviceId()Ljava/lang/String;'] = device_id
    functionToValueMap['Landroid/telephony/TelephonyManager;->getLine1Number()Ljava/lang/String;'] = line_number
    functionToValueMap['Landroid/telephony/TelephonyManager;->getDeviceSoftwareVersion()Ljava/lang/String;'] = device_software_version
    functionToValueMap['Landroid/telephony/TelephonyManager;->getSimSerialNumber()Ljava/lang/String;'] = sim_serial_number
    functionToValueMap['Landroid/telephony/TelephonyManager;->getSubscriberId()Ljava/lang/String;'] = subscriber_id
    functionToValueMap['Landroid/telephony/TelephonyManager;->getVoiceMailAlphaTag()Ljava/lang/String;'] = voicemail_alpha_tag
    functionToValueMap['Landroid/telephony/TelephonyManager;->getVoiceMailNumber()Ljava/lang/String;'] = voicemail_number
    functionToValueMap['Landroid/telephony/TelephonyManager;->listen(Landroid/telephony/PhoneStateListener;I)V'] = '[DELETE]'


if send_sms:
    functionToValueMap['Landroid/telephony/SmsManager;->sendTextMessage('] = '[DELETE]'
    functionToValueMap['Landroid/telephony/SmsManager;->sendDataMessage('] = '[DELETE]'
    functionToValueMap['Landroid/telephony/SmsManager;->sendMultipartTextMessage('] = '[DELETE]'


if read_logs:
    functionShimMap['Ljava/lang/Runtime;->exec([Ljava/lang/String;)Ljava/lang/Process;'] = 'exec'
    functionShimMap['Ljava/lang/Runtime;->exec([Ljava/lang/String;[Ljava/lang/String;)Ljava/lang/Process'] = 'exec'
    functionShimMap['Ljava/lang/Runtime;->exec([Ljava/lang/String;[Ljava/lang/String;Ljava/io/File;)Ljava/lang/Process'] = 'exec'
    functionShimMap['Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;'] = 'exec'
    functionShimMap['Ljava/lang/Runtime;->exec(Ljava/lang/String;[Ljava/lang/String;)Ljava/lang/Process'] = 'exec'
    functionShimMap['Ljava/lang/Runtime;->exec(Ljava/lang/String;[Ljava/lang/String;Ljava/io/File;)Ljava/lang/Process'] = 'exec'


if dynamicPermissionCheck:
    functionShimMap['Landroid/app/Activity;->checkCallingOrSelfPermission(Ljava/lang/String;)I'] = 'permcheck'
    functionShimMap[';->checkCallingOrSelfPermission(Ljava/lang/String;)I'] = 'permcheck'


if read_contacts:
    functionShimMap['Landroid/content/ContentResolver;->query(Landroid/net/Uri;[Ljava/lang/String;Ljava/lang/String;[Ljava/lang/String;Ljava/lang/String;)Landroid/database/Cursor;'] = 'contacts'


if get_accounts:
    functionShimMap['Landroid/accounts/AccountManager;->getAccounts()[Landroid/accounts/Account;'] = 'get_accounts'
    functionShimMap['Landroid/accounts/AccountManager;->getAccountsByType(Ljava/lang/String;)[Landroid/accounts/Account;'] = 'get_accounts'
    functionShimMap['Landroid/accounts/AccountManager;->getAccountsByTypeAndFeatures(Ljava/lang/String;[Ljava/lang/String;Landroid/accounts/AccountManagerCallback;Landroid/os/Handler;)Landroid/accounts/AccountManagerFuture;'] = 'get_accounts'
    functionShimMap['Landroid/accounts/AccountManager;->hasFeatures(Landroid/accounts/Account;[Ljava/lang/String;Landroid/accounts/AccountManagerCallback;Landroid/os/Handler;)Landroid/accounts/AccountManagerFuture;'] = 'get_accounts'
    functionToValueMap['Landroid/accounts/AccountManager;->addOnAccountsUpdatedListener(Landroid/accounts/OnAccountsUpdateListener;Landroid/os/Handler;Z)V'] = '[DELETE]'
    functionShimMap['Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;'] = 'reflect'


# This holds functions that we should be handling, but aren't.  If we encounter
# them, a message will be printed warning that they're present.
incompleteFunctions = ['managedQuery', 'CursorLoader']


# apktool doesn't like it when a directory already exists, so we'll create
# a secure temporary directory, then have it use the 'a' sub-directory.
topTempDir = tempfile.mkdtemp()
tempDir = topTempDir + '/new'
tempDirOrig = topTempDir + '/orig'

# Generate the signing key.
keystorePath = '%s/%s' % (topTempDir, 'keystore')
makeKeyStore(keystorePath)

v('Unpacking, decoding, and disassembling %s into %s... ' % (originalAPK, tempDir))

stdDestination = subprocess.PIPE
if verbose:
    stdDestination = None

p = subprocess.Popen(['java', '-jar', 'apktool.jar', 'decode', originalAPK,
                      tempDir], stdout=stdDestination, stderr=stdDestination,
                     close_fds=True)
p.wait()
v('Done.')

if keepFlag:
    v('Copying disassembled sources dir for diff\'ing later... ',)
    shutil.copytree(tempDir, tempDirOrig)
    v('Done.')



# Create a directory to hold any code files we create.
dedicatedDir = tempDir + '/smali/com/apptroller'
if not os.path.isdir(dedicatedDir):
    os.makedirs(dedicatedDir, 0700)


processedFiles = []  # Holds the list of smali files already processed.
reflectionFound = False
filesWithUnhandledMethods = []

nativeLibraryFound = False
for root, dirs, files in os.walk(tempDir): # + '/smali'):
    #print 'Stuff: %s %s %s' % (root, dirs, files)
    for f in files:
        if f.endswith('.so'):
            nativeLibraryFound = True
        elif f.endswith('.smali'):
            smaliPath = root + '/' + f
            modified = False
            d('Processing %s...' % smaliPath)

            hSmali = open(smaliPath, 'r')
            lines = hSmali.readlines()
            hSmali.close()
            code = ""

            variableValues = {}
            i = 0
            lastDotLocalsIndex = 0
            classPackage = None
            freeGotoIndex = 0

            catchBlocks = []
            #labels = {}

            while i < len(lines):
            #for i in range(0, len(lines)):
                #print "i: %d" % i
                line = lines[ i ]

                # Count the whitespace before the code starts in this line.
                spaces = ''
                j = 0
                while line[ j ] == ' ':
                    spaces = spaces + ' '
                    j = j + 1

                sline = line[len(spaces):]

                if sline.startswith('.class '):
                    pos1 = sline.find('L')
                    pos2 = sline.rfind('/')
                    if pos1 == -1:
                        raise Exception, 'Could not extract class package in [%s]' % sline
                    if pos2 == -1:
                        classPackage = '/'
                    else:
                        classPackage = sline[pos1+1:pos2]
                    #print "Class package: [%s]" % classPackage


                #if reflectionFound and sline.startswith('.method') and sline.find('<init>') == -1 and line.find('<clinit>') == -1:
                #    tokens = sline.split()
                #    if tokens[1] == 'protected' or tokens[1] == 'private':
                #        tokens[1] = 'public'
                #        modified = True
                #    elif tokens[1] != 'public':
                #        tokens.insert(1, 'public')
                #        modified = True

                #    lines[ i ] = ' '.join(tokens) + "\n"

                if sline.startswith('.locals '):
                    nextFreeVar = int(sline[8:])
                    lastDotLocalsIndex = i
                    #print '.locals: [%s][%d]' % (sline, nextFreeVar)

                if sline.startswith('const'):
                    tline = sline.strip()
                    startPos = tline.find(' ') + 1
                    endPos = tline.find(',', startPos)
                    var = tline[startPos:endPos]
                    val = tline[endPos+2:]
                    #print "X: [%s|%s]" % (var, val)
                    variableValues[var] = val



                #if sline.startswith(':'):
                #    labels[sline] = i

                # If this is an invoke- call, lets see if we need to intercept
                # the function...
                if sline.startswith('invoke-'):

                    if reflectionFound:
                        idPos = line.find('invoke-direct')
                        if idPos != -1 and sline.find('<init>') == -1 and line.find('<clinit>') == -1:
                            line = line[:idPos] + 'invoke-virtual' + line[idPos + 13:]
                            lines[ i ] = line
                            modified = True
                        

                    # Iterate over all values in our function map and see if
                    # any match.  If so, pull out the value that is supposed
                    # to be substituted.
                    subVal = None
                    for function in functionToValueMap.keys():
                        if sline.find(function) != -1:
                            subVal = functionToValueMap[function]
                            d("Found for substitution: %s -> %s" % (function, subVal))
                            lines[ i ] = ''

                    # If the value is [DELETE], then this function need only
                    # be removed; no substitution necessary.  This is used
                    # to remove callback registrations.
                    if subVal == '[DELETE]':
                        #print "Deleting this line..."
                        lines[ i ] = ''
                        modified = True

                    # If the target function's value in the dictionary is itself
                    # a dictionary, then we take this to mean that the function
                    # should be deleted if certain 
                    #elif type(subVal) is dict:
                    #    functionVariableNames = parseFunctionArgs(sline)
                    #    if CONDITIONAL_DELETE_ARG_1 in subVal:
                    #        if variableValues[functionVariableNames[0]] in subVal[CONDITIONAL_DELETE_ARG_1]:
                    #            lines[ i ] = ''
                    #            modified = True

                    # If we found a value to substitute...
                    elif subVal is not None:
                        # Skip all subsequent empty lines until a non-empty one
                        # is found.  Too bad Python doesn't have a do..while
                        # loop...
                        while True:
                            i = i + 1
                            line = lines[ i ].strip()

                            # Skip over empty lines, labels, and catch lines.
                            if (line != '') and (not line.startswith(':')) and (not line.startswith('.catch')):
                            #if line.strip() != '':
                                break

                        # We parse out the variable name in the subsequent
                        # move-result-object call.  That variable name
                        # we will set to a constant value.
                        pos = line.find('move-result-object ')
                        varName = None
                        if pos != -1:
                            varType = None
                            if type(subVal) is str:
                                varType = 'string'

                            varName = line[pos + 19:].strip()
                            line = spaces + 'const-%s %s, "%s"\n' % (varType, varName, subVal)
                            lines[ i ] = line
                            modified = True
                        else:
                            e('could not find move-result-object! [%s]' % line, True)
                            

                    for function in functionShimMap.keys():
                        if sline.find(function) != -1:
                            d('Found function to shim!: %s' % sline)
                            shimtype = functionShimMap[function]

                            if shimtype == 'exec':
                                modifiedFlag = ShimExec.shim(root, classPackage, lines, i, readLogsStdout, readLogsStderr)
                                lineDifference = 0
                            elif shimtype == 'permcheck':
                                modifiedFlag = ShimDynamicPermissionCheck.shim(root, classPackage, lines, i, neuteredPermissions)
                            elif shimtype == 'contacts':
                                modifiedFlag = ShimReadContacts.shim(root, classPackage, lines, i)
                            elif shimtype == 'get_accounts':
                                modifiedFlag = ShimGetAccounts.shim(dedicatedDir, 'com/apptroller', lines, i, googleAccount)
                            elif shimtype == 'reflect':
                                #if reflectionFound == False:
                                #    filesWithUnhandledMethods = list(processedFiles)
                                #    filesWithUnhandledMethods.append(smaliPath)
                                    #print "XXX: ",
                                    #print filesWithUnhandledMethods
                                    #sys.exit(1)
                                #reflectionFound = True
                                modifiedFlag = ShimReflection.shim(dedicatedDir, 'com/apptroller', lines, i, googleAccount)

                            modified = modified or modifiedFlag
                            #print lines
                            #sys.exit(1)


                    # Check if theres a function in use that we don't handle,
                    # but should.  In that case, we'll print to stdout and
                    # continue, but the resulting APK might not work...
                    for function in incompleteFunctions:
                        if sline.find(function) != -1:
                            e('Found function that we\'re not handling!: %s (in %s)' % (function, smaliPath), False)

                #code = code + line
                i = i + 1

            if modified:
                pp = PostProcessor()
                pp.process(lines)
                d('    Modified: %s' % smaliPath)
                hSmali = open(smaliPath, 'w')
                hSmali.write(''.join(lines))
                hSmali.close()
            #else:
            #    print '    Not modified: %s' % smaliPath
            processedFiles.append(smaliPath)



#if reflectionFound:
#    makeAllMethodsPublic(filesWithUnhandledMethods)

v('Removing permissions from manifest file... ',)
newManifestXML = ''
hManifest = open(tempDir + '/AndroidManifest.xml', 'r')
manifestXML = "".join(hManifest.readlines())
hManifest.close()

deletedLines = []
#for line in hManifest:
for line in iter(manifestXML.splitlines()):
    removeIt = False
    for permission in neuteredPermissions:
        if line.find(permission) != -1:
            removeIt = True
            deletedLines.append(permission)

    if removeIt == False:
        newManifestXML += line + "\n"
#hManifest.close()
#print ''

# A block of XML needs to be removed if we're neutering RECEIVE_SMS.
if receive_sms:
    filterRegex = re.compile(r'<receiver.*?"android.provider.Telephony.SMS_RECEIVED".*?</receiver>', re.S)
    newManifestXML = filterRegex.sub('', newManifestXML)

# If we're supposed to enable application debugging in the manifest...
if enableDebug:

    # Extract the <application> element...
    appStart = newManifestXML.find('<application ')
    appEnd = newManifestXML.find('>', appStart)
    appLine = newManifestXML[appStart:appEnd]
    #print 'APPLINE: [%s]' % appLine
    
    # Find the "debuggable" attribute value, and change it to true if necessary
    newAppLine = ''
    debugStart = appLine.find('android:debuggable="')
    if debugStart != -1:
        debugEnd = appLine.find('"', debugStart + 21)
        debugVal = appLine[debugStart + 20:debugEnd]
        #print "DV: [%s]" % debugVal

        # Debugging is explicitly set to false, so we'll change that to true.
        if debugVal == 'false':
            newAppLine = appLine[:debugStart + 20] + 'true' + appLine[debugEnd:]
            #print "NAL: [%s]" % newAppLine

    else: # The debuggable attribute was not explicitly set, so we'll set it...
        newAppLine = appLine + ' android:debuggable="true"'

    newManifestXML = newManifestXML[:appStart] + newAppLine + newManifestXML[appEnd:]
    #print "NEW MANIFEST: [%s]" % newManifestXML



if len(deletedLines) > 0:
    v("Removed permissions from manifest file:\n   %s" % "\n   ".join(deletedLines))
else:
    e('Error: no permission were removed from manifest file!', True)


hManifest = open(tempDir + '/AndroidManifest.xml', 'w')
#print newManifestXML
hManifest.write(newManifestXML)
hManifest.close()
v('Done modifying manifest file.')


tempAPK = topTempDir + '/temp.apk'
v('Encoding and re-assembling %s into %s... ' % (tempDir, tempAPK))

stdDestination = subprocess.PIPE
if verbose:
    stdDestination = None

p = subprocess.Popen(['java', '-jar', 'apktool.jar', 'build', tempDir,
                      tempAPK], stdout=stdDestination, stderr=stdDestination,
                     close_fds=True)
p.wait()
v('Done encoding and re-assembling.')

if keepFlag:
    diffPath = topTempDir + '/diff.txt'
    v('Creating diff in %s ... ' % diffPath,)
    hDiff = open(diffPath, 'w')
    p = subprocess.Popen(['diff', '-ru', tempDirOrig, tempDir], stdout=hDiff, close_fds=True)
    p.wait()
    hDiff.close()
    v('Done creating diff.')


v('Signing %s... ' % tempAPK,)
p = subprocess.Popen(['jarsigner', '-keystore', keystorePath, '-storepass', 'abcdef', tempAPK, 'lol'], close_fds=True)
p.wait()
v('Done.')

v('Aligning %s to %s... ' % (tempAPK, outputAPK),)
stdoutDestination = subprocess.PIPE
if verbose:
    stdoutDestination = None
p = subprocess.Popen(['zipalign', '-f', '4', tempAPK, outputAPK], stdout=stdoutDestination, close_fds=True)
p.wait()
v('Done.')


if keepDiff is not None:
    v('Moving diff file from %s/diff.txt to %s...' % (topTempDir, keepDiff))
    os.rename('%s/diff.txt' % topTempDir, '%s' % keepDiff)

    # Set the keep flag to false so that the dir is deleted below.
    keepFlag = False

# Delete the directory containing all disassembled files, unless the user
# wants to keep it.
if keepFlag is not True:
    v('Removing disassembled sources directory %s... ' % topTempDir,)
    shutil.rmtree(topTempDir)
    v('Done.')
else:
    print 'Disassembled sources are in %s' % topTempDir

if nativeLibraryFound:
    print "\nWARNING: Native code detected!  Any privileged access calls within are not yet sanitized, and will cause an application crash (because permissions are removed from manifest)."

if not os.path.exists(outputAPK):
    print "\nERROR: Output APK file (%s) was not created; there is a problem with re-assembly.  Re-run with the -d flag for more information.\n" % outputAPK
