# ===================================================================================================
# Imports: External
# ===================================================================================================
import os
import wx

# ===================================================================================================
# Imports: Internal
# ===================================================================================================

from .abs_gui import MainFrame
from .pakbuilder import PakBuilder

# ===================================================================================================
# KCD Paker GUI Class
# ===================================================================================================
class KCDPakBuilderGui(MainFrame):
    '''
    KCD Paker GUI
    '''



    def __init__(self, version, author):
        '''
        Constructor
        '''
        self._version = version
        self._author = author
        self._paker = None
        super(KCDPakBuilderGui, self).__init__(None)

        # Set Up GUI
        self._bind_events()
        self._init_ui()

    def _bind_events(self):
        '''
        Binds Gui Events
        '''
        self.Bind(wx.EVT_BUTTON, self._on_start_pak, self.btn_start_pak)
        self.Bind(wx.EVT_BUTTON, self._on_stop_pak, self.btn_stop_pak)

    def _init_ui(self):
        '''
        Update and override any UI parameters post parent initialisation
        '''
        self.SetTitle("KCD PAK Builder (v%s) by %s" % (self._version, self._author))

        # Update Icon
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(self._get_icon_path()))
        self.SetIcon(icon)

    def _on_start_pak(self, event):
        '''
        Start/Build PAK Button Callback. Called when Build PAK Button is clicked. Initiates PAK Build

        :param event: wx Click Event
        '''
        # Process Inputs
        pak_path = self.fp_pak_out_path.GetPath()
        target_dir = self.dp_target_dir.GetPath()

        # Update UI
        self.btn_stop_pak.Enable()
        self.btn_start_pak.Disable()
        self.output_log.Clear()

        # Initialise PAK Builder
        self._paker = PakBuilder(self, pak_path, target_dir)
        self._paker.build_filelist()
        self.pak_pg_bar.SetRange(self._paker.get_total_file_count())

        # Start Pak!
        self._paker.start_pak()

    def _on_stop_pak(self, event):
        '''
        Stop Build Button Callback. Called when Stop button is clicked. Stops the build

        :param event: wx Click Event
        '''
        self._paker.stop_pak()
        self.btn_stop_pak.Disable()
        self.btn_start_pak.Enable()

    def on_file_processed(self, file):
        '''
        File Processed Callback. To be called by PakBuilder instance when it successfully processes a file

        :param file: The file that was just processed
        :type file: str
        '''

        # Update Progress Bar
        self.pak_pg_bar.SetValue(self.get_paker().get_processed_file_count())

        # Update Status
        total_files = self.get_paker().get_total_file_count()
        files_processed = self.get_paker().get_processed_file_count()
        percent_completion = int((files_processed / total_files) * 100)
        if files_processed == total_files:
            new_status = "Build Finished! (100%)"
        elif self.get_paker().was_stopped():
            new_status = "Cancelled"
            self.pak_pg_bar.SetValue(0)
        else:
            new_status = "%s of %s (%s%%)" % (total_files, files_processed, percent_completion)
        self.label_status.SetLabel(new_status)

        # Log file
        log_msg = "[+] %s\n" % file
        self.output_log.write(log_msg)


    # ===================================================================================================
    # Getters
    # ===================================================================================================
    def get_paker(self) -> PakBuilder:
        '''
        Gets the current Paker Instance

        :return: The current Paker Instance
        :rtype: PakBuilder
        '''
        return self._paker


    # ===================================================================================================
    # Internal Helpers
    # ===================================================================================================
    def _get_icon_path(self):
        '''
        Gets the path to the GUI Icon (.ico) file

        :return: The path to the GUI Icon File
        :rtype: str
        '''
        cwd = os.getcwd()
        icon_path = None

        if "_MEI" in __file__: # (Packed)
            icon_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "resources", "icon.ico"
            )
        else: # (Not Packed)
            icon_path = os.path.join(os.path.dirname(__file__), "resources", "icon.ico")

        return icon_path
