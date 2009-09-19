import sys
import os

# Script constants
__scriptname__ = "The Big Picture"
__author__ = "rwparris2"
__url__ = "http://code.google.com/p/xbmc-addons/"
__credits__ = "Team XBMC"
__version__ = "0.9.0"

print "[SCRIPT] '%s: version %s' initialized!" % (__scriptname__, __version__)

if ( __name__ == "__main__" ):
    import resources.lib.gui as gui
    ui = gui.GUI( "main.xml", os.getcwd(), "default" )
    ui.doModal()
    del ui
    sys.modules.clear()