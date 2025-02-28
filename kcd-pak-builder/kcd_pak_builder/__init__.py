# ===================================================================================================
# Imports: External
# ===================================================================================================
import wx
from wx._core import wxAssertionError

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .gui import KCDPakBuilderGui

# ===================================================================================================
# Properties
# ===================================================================================================
VERSION = "1.3.0"
AUTHOR  = "Altire"


# ===================================================================================================
# KCD PAK Builder Class
# ===================================================================================================
class KCDPakBuilder():
    '''
    KCD PAK Builder. Main object for KCD PAK Builder Package
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Initialise the GUI
        self._app = wx.App()
        self._gui = KCDPakBuilderGui(VERSION, AUTHOR)

    def launch(self):
        '''
        Launches the PAK Builder GUI
        '''
        self._gui.Show()
        # Ignore wx Assertion Failures
        try:
            self._app.MainLoop()
        except wxAssertionError as ex:
            print("WX Assertion error (Likely during app close): %s" % ex)