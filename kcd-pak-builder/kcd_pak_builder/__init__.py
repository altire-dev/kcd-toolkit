import wx
from .gui import KCDPakerGui

class KCDPaker():
    '''
    KCD Paker
    '''

    def __init__(self):
        '''
        Constructor
        '''

        # Initialise the Builder GUI
        self._app = wx.App()
        self._gui = KCDPakerGui()

    def launch(self):
        '''
        Launches the Builder GUI
        '''

        self._gui.Show()
        self._app.MainLoop()