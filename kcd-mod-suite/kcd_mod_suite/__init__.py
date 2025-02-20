# ===================================================================================================
# Imports: External
# ===================================================================================================
import wx

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
        self._app.MainLoop()
