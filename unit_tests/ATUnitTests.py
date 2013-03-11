'''
ATUnitTests.py
Copyright (C) 2012, Joe Testa <jtesta@positronsecurity.com>

This runs the unit tests for AppTroller.


TODO:  * close subprocess handles
       * chdir() should restore original path, not 'unit_test' 
       * implement verbose mode.
'''

import getopt, os, subprocess, sys


# Sends an error message to stderr.  If the 'term' argument is True, terminate
# the program.
def e(msg, term):
    print >> sys.stderr, 'Error: %s' % msg
    if term:
        sys.exit(1)


# Sends a verbose message to stdout if the verbose flag is set.
def v(msg):
    if verbose:
        print msg


# A diff file normally contains specific path information and timestamps.
# These are unique per each invokation, so they must be stripped out so that
# the diffs can be compared in a byte-by-byte fashion.
#
# This function reads a specified diff file and returns cleaned content in a
# string.  The argument file is not modified.
def cleanDiffFile(diffFile):
    hDiff = open(diffFile, 'r')
    diffLines = hDiff.readlines()
    hDiff.close()


    i = 0
    while i < len(diffLines):
	# Remove the specific path information. i.e.:
	# diff -ru /tmp/tmpJ37osP/orig/AndroidManifest.xml /tmp/tmpJ37osP/new/AndroidManifest.xml
	# =>
	# diff -ru orig/AndroidManifest.xml new/AndroidManifest.xml
        line = diffLines[ i ]
        if line.startswith('diff -ru '):
            tmpPaths = line.strip()[9:].split(' ')
            path1 = cleanTempPath(tmpPaths[0])
            path2 = cleanTempPath(tmpPaths[1])
            line = "diff -ru %s %s\n" % (path1, path2)
	# Remove the specific path information and timestamp. i.e.:
        # --- /tmp/tmpJ37osP/orig/AndroidManifest.xml	2012-05-31 23:46:51.891757000 -0400
	# =>
	# --- orig/AndroidManifest.xml
        elif line.startswith('--- '):
            tokens = line.split(' ')
            path = cleanTempPath(tokens[1].split('\t')[0])
            line = "--- %s\n" % path
        # i.e.:
	# +++ /tmp/tmpJ37osP/new/AndroidManifest.xml	2012-05-31 23:46:52.041754813 -0400
	# =>
	# +++ new/AndroidManifest.xml
        elif line.startswith('+++ '):
            tokens = line.split(' ')
            path = cleanTempPath(tokens[1].split('\t')[0])
            line = "+++ %s\n" % path
	# i.e.:
        # Only in /tmp/tmpJ37osP/new/smali/com/apptroller/readlogs: LolExec.smali
	# =>
	# new/smali/com/apptroller/readlogs: LolExec.smali
        elif line.startswith('Only in '):
            tokens = line.split(' ')
            path = cleanTempPath(tokens[2])
            line = 'Only in %s ' % path

            j = 3
            while j < len(tokens):
                line = line + ' ' + tokens[ j ]
                j = j + 1

        diffLines[ i ] = line
        i = i + 1

    ret = ''.join(diffLines)

    # Over-write the diff file with the cleaned version.
    hDiff = open(diffFile, 'w')
    hDiff.write(ret)
    hDiff.close()

    # Return the cleaned contents.
    return ret


# For a path like '/tmp/tmpADGds9/one/two/three', strip out the first two
# directories and return 'one/two/three'.
def cleanTempPath(tmpPath):
    # For the example above, this split returns the following list:
    # ['', 'tmp', 'tmpADGds9', 'one', 'two', 'three']
    dirs = tmpPath.split('/')
    del dirs[0]  # This actually deletes an empty string.
    del dirs[0]
    del dirs[0]
    return '/'.join(dirs)


def usage(exitval):
    print
    print
    print 'ATUnitTests.py'
    print
    print 'Usage: python ATUnitTests.py [OPTIONS]'
    print
    print
    print "  -g, --generate    Generate a new unit test using a specified APK."
    print "  -t, --test        Run a specific unit test (default is all)."
    print "  -v, --verbose     Enable verbose output."
    print
    print
    sys.exit(exitval)


# This will generate a diff file for the specified APK.  If mode is 'generate',
# the diff will be saved to the path referenced by testAPK with '.diff'
# appended; this becomes the authoritative diff.  Otherwise, if mode is 'test',
# the generated diff is compared to the authoritative diff.
#
# When mode is 'generate', returns True if the authoritative diff was
# successfully created, or False if it was not.  When mode is 'test', returns
# True when the generated diff and authoritative diff match, or False when they
# do not.
def generateDiff(testAPK, mode):
    ret = False

    # Check that the APK file is readable.
    hTest = None
    try:
        hTest = open(testAPK, 'r')
    except:
        e('Could not open %s for reading!', True)
    finally:
        if hTest is not None:
            hTest.close()

    # Check if this APK has a corresponding configuration file.
    configFile = '%s.cfg' % testAPK
    if not os.path.exists(configFile):
        configFile = None
    else:
        v('Config file for %s found.' % testAPK)

    #outputAPK = '/dev/null'

    # Remove the temp output file if it exists from a previous invokation.
    if os.path.exists('tmp.apk'):
	os.unlink('tmp.apk')
    #os.mkdir('tmp')

    # The output APK goes into the temporary directory.
    outputAPK = 'unit_tests/tmp.apk'

    # Change the current directory to the parent directory, since that is where
    # AppTroller.py lives.  We will then run it from within its directory.
    os.chdir('..')


    if mode == 'generate':
        v('Generating diff for %s...' % testAPK)

	# Remove any existing authoritative diff file since we are about to
	# make a new one.
	outputDiffPath = 'unit_tests/%s.diff' % testAPK
	if os.path.exists(outputDiffPath):
	    os.unlink(outputDiffPath)

        v('Running AppTroller...')

        argList = ['python', 'AppTroller.py', '-K', outputDiffPath]
        if configFile is not None:
            argList.extend(['-c', 'unit_tests/%s' % configFile])
        argList.extend(['unit_tests/%s' % testAPK, outputAPK])

	# Run AppTroller on the specified APK, save the diff file in its final
	# resting place.
        p = subprocess.Popen(argList)
        p.wait()

        v('Done.')

	# Clean the resulting diff file of timestamps and absolute path
	# path information since these will always be different in subsequent
	# runs (leaving them in would always cause a unit test failure).
        cleanDiff = cleanDiffFile(outputDiffPath)

	print 'Generated diff file at: %s' % outputDiffPath
	ret = True
    elif mode == 'test':
        v('Testing %s...' % testAPK)


        v('Running AppTroller...')
	authDiffPath = 'unit_tests/%s.diff' % testAPK
	tempDiffPath = '%s.failed' % authDiffPath


        argList = ['python', 'AppTroller.py', '-K', tempDiffPath]
        if configFile is not None:
            argList.extend(['-c', 'unit_tests/%s' % configFile])
        argList.extend(['unit_tests/%s' % testAPK, outputAPK])

        p = subprocess.Popen(argList)
        p.wait()
        v('Done.')

	# Get the clean version of the diff we just created.
        tempDiff = cleanDiffFile(tempDiffPath)
 
	# Get the authoritative diff.
        hDiff = open(authDiffPath, 'r')
        authDiff = hDiff.read()
        hDiff.close()

	# If the length of the current diff and authoritative diff do not
        # match, then (obviously), they're not the same.
	same = True
        if len(tempDiff) != len(authDiff):
            print "%d %d" % (len(tempDiff), len(authDiff))
	    same = False

	# Compare each byte of the current and authoritative diffs.  Stop at
	# the first mismatch, or if the end is reached.
	i = 0
	while (same == True) and (i < len(authDiff)):
            if tempDiff[ i ] != authDiff[ i ]:
	        same = False
                print "DIFF AT %d" % i
	    i = i + 1

	# If they're the same, delete the diff we just made.  Otherwise, we
	# keep it so the user can manually inspect why the test failed.
	if same:
	    os.unlink(tempDiffPath)
	    print '%s: passed.' % testAPK
	else:
            e('%s: FAILED!  Diff is in: %s' % (testAPK, tempDiffPath), False)

	ret = same
    else:
        e('Invalid mode!: %s' % mode, True)

    os.unlink(outputAPK)

    # Restore the current directory to what it was when we began.  Remove the
    # temporary directory.
    os.chdir('unit_tests')
    #shutil.rmtree('tmp')
    return ret


# Runs all unit tests and returns the number that failed.
def runAllTests():
    failed = 0
    for root, dirs, files in os.walk('.'):
	for file in files:
            if file.endswith('.apk.diff'):
                v('Found diff: %s' % file)
		if not generateDiff(file[:-5], 'test'):
		    failed = failed + 1

    if failed == 0:
	print 'All tests pass!'
    elif failed == 1:
        e('1 test failed!', False)
    else:
	e('%d tests failed!' % failed, False)

    return failed


opts = None
args = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "t:g:hv", ["test=", "generate=", "help", "verbose"])
except getopt.GetoptError, err:
    print
    print str(err)
    usage(1)

testAPK = None
generateOnAPK = None
verbose = False
for o, a in opts:
    if o in ('-t', '--test'):
        testAPK = a
    elif o in ('-g', '--generate'):
        generateOnAPK = a
    elif o in ('-h', '--help'):
        usage(0)
    elif o in ('-v', '--verbose'):
        verbose = True


exitCode = 0
if generateOnAPK is not None:
    if not generateDiff(generateOnAPK, 'generate'):
	exitCode = 2
elif testAPK is not None:
    if not generateDiff(testAPK, 'test'):
	exitCode = 2
else:
    if runAllTests() > 0:
	exitCode = 2

sys.exit(exitCode)

