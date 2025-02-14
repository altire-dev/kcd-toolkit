# ===================================================================================================
# Imports: External
# ===================================================================================================
import wx

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .gui import KCDModGeneratorGui

# ===================================================================================================
# KCD Mod Generator Class
# ===================================================================================================
class KCDModGenerator():
    '''
    KCD Mod Generator. Main object for KCD Mod Generator Package
    '''

    def __init__(self, version, author):
        '''
        Constructor
        '''
        # Initialise the GUI
        self._app = wx.App()
        self._gui = KCDModGeneratorGui(version, author)

    def launch(self):
        '''
        Launches the app
        '''
        self._gui.Show()
        self._app.MainLoop()