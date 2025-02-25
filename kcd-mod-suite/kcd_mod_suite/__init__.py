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
# KCD Mod Suite Class
# ===================================================================================================
class KCDModSuite():
    '''
    KCD Mod Suite. Main object for KCD Mod Suite Package
    '''

    def __init__(self, version, author):
        '''
        Constructor
        '''
        # Initialise the GUI
        self._app = wx.App()
        self._gui = KCDModSuiteGui(version, author)

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
