import wx

from .abs_gui import MainFrame
from .paker import Paker

class KCDPakerGui(MainFrame):

    def __init__(self):
        '''
        Constructor
        '''
        self._paker = None
        super(KCDPakerGui, self).__init__(None)

        self._bind_events()

    def _bind_events(self):
        '''
        Binds Gui Events
        :return:
        '''
        self.Bind(wx.EVT_BUTTON, self._on_start_pak, self.btn_start_pak)
        self.Bind(wx.EVT_BUTTON, self._on_stop_pak, self.btn_stop_pak)

    def _on_start_pak(self, event):
        pak_path = self.fp_pak_out_path.GetPath()
        target_dir = self.dp_target_dir.GetPath()
        self._paker = Paker(self, pak_path, target_dir)
        self._paker.start_pak()

    def _on_stop_pak(self, event):
        self._paker.stop_pak()
