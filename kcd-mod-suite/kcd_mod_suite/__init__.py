# ===================================================================================================
# Imports: External
# ===================================================================================================
import wx
from wx._core import wxAssertionError

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .gui import KCDModSuiteGui

# ===================================================================================================
# Properties
# ===================================================================================================
VERSION = "0.1.1"
AUTHOR  = "Altire"

# ===================================================================================================
# KCD Mod Suite Class
# ===================================================================================================
class KCDModSuite():
    '''
    KCD Mod Suite. Main object for KCD Mod Suite Package
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Initialise the GUI
        self._app = wx.App()
        self._gui = KCDModSuiteGui(VERSION, AUTHOR)

    def launch(self):
        '''
        Launches the app
        '''
        self._gui.Show()
        # Ignore wx Assertion Failures
        try:
            self._app.MainLoop()
        except wxAssertionError as ex:
            print("WX Assertion error (Likely during app close): %s" % ex)
