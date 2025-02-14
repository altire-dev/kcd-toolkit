# ===================================================================================================
# Imports: External
# ===================================================================================================
import wx

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .gui import KCDModInitialiserGui

# ===================================================================================================
# KCD Mod Initialser Class
# ===================================================================================================
class KCDModInitialiser():
    '''
    KCD Mod Initialser. Main object for KCD Mod Initialser Package
    '''

    def __init__(self, version, author):
        '''
        Constructor
        '''
        # Initialise the GUI
        self._app = wx.App()
        self._gui = KCDModInitialiserGui(version, author)

    def launch(self):
        '''
        Launches the PAK Builder GUI
        '''
        self._gui.Show()
        self._app.MainLoop()