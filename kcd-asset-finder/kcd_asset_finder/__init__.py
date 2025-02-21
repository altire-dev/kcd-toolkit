# ===================================================================================================
# Imports: External
# ===================================================================================================
import wx

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .gui import KCDAssetFinderGui

# ===================================================================================================
# Properties
# ===================================================================================================
VERSION = "0.1.0"
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
        self._app.MainLoop()
