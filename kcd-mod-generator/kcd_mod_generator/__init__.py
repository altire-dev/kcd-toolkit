# ===================================================================================================
# Imports: External
# ===================================================================================================
import wx
from wx._core import wxAssertionError

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .gui import KCDModGeneratorGui

# ===================================================================================================
# Properties
# ===================================================================================================
VERSION = "1.2.0"
AUTHOR = "Altire"


# ===================================================================================================
# KCD Mod Generator Class
# ===================================================================================================
class KCDModGenerator:
    '''
    KCD Mod Generator. Main object for KCD Mod Generator Package
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
        self._gui = KCDModGeneratorGui(VERSION, AUTHOR)

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
