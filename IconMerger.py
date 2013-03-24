'''
IconMerger.py
Copyright (C) 2013, Joe Testa <jtesta@positronsecurity.com>

This class merges an app's normal icon with TrollFace.  ;)
'''

import os, subprocess

class IconMerger:


    # Filesystem paths to variously-sized TrollFaces.
    TF_90 = 'icons/tf_90.png'
    TF_72 = 'icons/tf_72.png'
    TF_64 = 'icons/tf_64.png'
    TF_60 = 'icons/tf_60.png'
    TF_48 = 'icons/tf_48.png'
    TF_36 = 'icons/tf_36.png'


    def __init__(self, verbose, debug):
        self.verbose = verbose
	self.debug = debug


    # Sends an error message to stderr.
    def e(self, msg):
        print >> sys.stderr, 'Error: %s' % msg


    # Sends a debugging message to stdout if the debugging flag is set.
    def d(self, msg):
        if self.debug:
            print msg


    # Sends a verbose message to stdout if the verbose flag is set.
    def v(self, msg):
        if self.verbose:
            print msg


    # Returns True if Imagemagick is installed and usable, False if it is not.
    def hasPrerequisites(self):
        ret = True

        try:
            subprocess.check_output(['identify', '-version'])
            subprocess.check_output(['composite', '-version'])
        except OSError:
            ret = False

        return ret


    # Given a top-level directory (which contains the 'res/' directory), and a
    # base icon name (i.e.: when defined with 'android:icon="@drawable/icon"',
    # "icon" is the base icon name), look for all the applicable image
    # directories and add the appropriately-sized TrollFace to each discovered
    # icon.
    #
    # Returns True on success, or False on failure.
    def addTrollFace(self, decodeDir, basename):
        ret = True

        self.d('addTrollFace(%s, %s)' % (decodeDir, basename))

        # Several icons of differing resolutions may be included.  We will find
        # them all and modify each one.
        for drawablePath in ('/res/drawable/', '/res/drawable-hdpi/', '/res/drawable-mdpi/', '/res/drawable-ldpi/'):

            # Icons are usually PNGs, but JPGs could also be used...
            for extension in ('.png', '.jpg'):

                # See if this path exists.  If so, we found an icon to modify!
                iconPath = decodeDir + drawablePath + basename + extension
                if os.path.exists(iconPath):
                    self.d('Found icon: %s' % iconPath)

                    # Get the max(height, width) of the icon.  We'll use this to
                    # determine the best sized TrollFace to overlay.
                    dimension = self.getDimension(iconPath)
                    if dimension == -1:
                        self.e('could not get the dimensions of %s. Skipping.' % iconPath)
                    else:
                        trollFacePath = IconMerger.TF_36
                        if dimension >= 90:
                            trollFacePath = IconMerger.TF_90
                        elif dimension >= 72:
                            trollFacePath = IconMerger.TF_72
                        elif dimension >= 64:
                            trollFacePath = IconMerger.TF_64
                        elif dimension >= 60:
                            trollFacePath = IconMerger.TF_60
                        elif dimension >= 48:
                            trollFacePath = IconMerger.TF_48
                        elif dimension >= 36:
                            trollFacePath = IconMerger.TF_36
                        
                        self.d('Picked icon %s for %s (with dimension %d)' % (trollFacePath, iconPath, dimension))
                        ret = ret & self.mergeIcons(iconPath, trollFacePath)
                        if not ret:
                            self.e('Icon merge for %s failed!' % iconPath)

        return ret


    # Given a filesystem path to an icon file, get its height and width in
    # pixels, and return max(height, width), or -1 on error.
    def getDimension(self, iconPath):

        # We will use Imagemagick's 'identify' command to find the height and
        # width of the icon.  Example output is:
        #
        # drawable/icon.png PNG 64x64 64x64+0+0 8-bit DirectClass 7.57KB 0.000u 0:00.000
        #
        # We will parse out the "64x64" string in the third field...
        output = subprocess.check_output(['identify', iconPath])
        firstSpace = output.find(' ')
        if firstSpace == -1:
            return -1

        secondSpace = output.find(' ', firstSpace + 1)
        if secondSpace == -1:
            return -1

        thirdSpace = output.find(' ', secondSpace + 1)
        if thirdSpace == -1:
            return -1

        dimensions = output[secondSpace + 1:thirdSpace]

        xPos = dimensions.find('x')
        if xPos == -1:
            return -1

        height = int(dimensions[:xPos])
        width = int(dimensions[xPos + 1:])

        self.d('Icon %s has dimensions %dx%d.' % (iconPath, height, width))

        return max(height, width)


    # Merge TrollFace onto the existing icon.  Return True on success, or False
    # on failure.
    def mergeIcons(self, iconPath, trollFacePath):
        output = subprocess.check_output(['composite', trollFacePath, iconPath, iconPath])
        if output == '':
            return True
        else:
            return False
