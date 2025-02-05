# ===================================================================================================
# Imports: External
# ===================================================================================================
import wx

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .gui import KCDPakBuilderGui

# ===================================================================================================
# KCD PAK Builder Class
# ===================================================================================================
class KCDPakBuilder():
    '''
    KCD PAK Builder. Main object for KCD PAK Builder Package
    '''

    def __init__(self, version, author):
        '''
        Constructor
        '''
        # Initialise the GUI
        self._app = wx.App()
        self._gui = KCDPakBuilderGui(version, author)

    def launch(self):
        '''
        Launches the PAK Builder GUI
        '''
        self._gui.Show()
        self._app.MainLoop()