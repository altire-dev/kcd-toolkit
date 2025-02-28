# ===================================================================================================
# Imports: External
# ===================================================================================================
import wx
from wx._core import wxAssertionError

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .gui import KCDAssetFinderGui

# ===================================================================================================
# Properties
# ===================================================================================================
VERSION = "1.3.0"
AUTHOR = "Altire"

# ===================================================================================================
# KCD Mod Generator Class
# ===================================================================================================
class KCDAssetFinder:
    '''
    KCD Asset Finder. Main object for KCD Asset Finder Package
    '''

    # ===================================================================================================
    # Methods
    # ===================================================================================================
    def __init__(self):
        '''
        Constructor
        '''
        # Initialise the GUI
        self._app = wx.App()
        self._gui = KCDAssetFinderGui(VERSION, AUTHOR)

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
