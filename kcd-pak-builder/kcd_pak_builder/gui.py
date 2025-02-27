# ===================================================================================================
# Imports: External
# ===================================================================================================
import json
import os
import wx
import re

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

    # ===================================================================================================
    # Properties
    # ===================================================================================================
    CFG_KEY_OUTPUT_DIR          = "pak_out_dir"
    CFG_KEY_PAK_FILENAME        = "pak_filename"
    CFG_KEY_TARGET_DIR          = "target_dir"
    CFG_KEY_IGNORE_NESTED_PAKS  = "ignore_nested_paks"
    CFG_KEY_SHOW_OPTIONS        = "show_options"
    CFG_KEY_MAX_PAK_MB          = "max_pak_mb"

    DEFAULT_PAX_MAX_MB          = 1900

    # ===================================================================================================
    # Methods
    # ===================================================================================================

    def __init__(self, version, author, suite=None):
        '''
        Constructor

        :param version: The app version
        :type version: str
        :param author: The app author
        :type author: str
        :param suite: Optional reference to parent Mod Suite application. To be passed if running as part of KCD Mod Suite
        :type suite: KCDModSuite
        '''
        self._version = version
        self._author = author
        self._paker = None

        # Load Configuration
        self._cfg_path = self._get_cfg_path()
        self._cfg = self._load_cfg()
        self._options_visible = self._cfg.get(self.CFG_KEY_SHOW_OPTIONS, True)

        # Initialise Frame
        super(KCDPakBuilderGui, self).__init__(suite)

        # Set Up GUI
        self._bind_events()
        self._init_ui()
        # self.write_to_log("[+] Config File Loaded: %s" % self._cfg_path)

    def _bind_events(self):
        '''
        Binds Gui Events
        '''
        bind_target = self
        if self.GetParent():
            bind_target = self.GetParent()

        # Button Events
        bind_target.Bind(wx.EVT_BUTTON, self._on_start_pak, self.btn_start_pak)
        bind_target.Bind(wx.EVT_BUTTON, self._on_stop_pak, self.btn_stop_pak)
        bind_target.Bind(wx.EVT_BUTTON, self._on_toggle_options, self.btn_toggle_options)

        # Checkbox Events
        bind_target.Bind(wx.EVT_CHECKBOX, self._on_save_filename_cb, self.cb_save_filename)
        bind_target.Bind(wx.EVT_CHECKBOX, self._on_save_output_dir_cb, self.cb_save_output_dir)
        bind_target.Bind(wx.EVT_CHECKBOX, self._on_save_target_dir_cb, self.cb_save_target_dir)
        bind_target.Bind(wx.EVT_CHECKBOX, self._on_ignore_nested_cb, self.cb_ignore_nested_paks)

        # Input Change Events
        bind_target.Bind(wx.EVT_DIRPICKER_CHANGED, self._on_output_dir_change, self.dp_pak_out_dir)
        bind_target.Bind(wx.EVT_TEXT, self._on_pak_filename_change, self.text_pak_filename)
        bind_target.Bind(wx.EVT_DIRPICKER_CHANGED, self._on_target_dir_change, self.dp_target_dir)
        bind_target.Bind(wx.EVT_TEXT, self._on_pak_max_mb_change, self.text_pak_max_mb)
        dt = DropTarget(self)
        self.Panel_QuickPack.SetDropTarget(dt)

    def _init_ui(self):
        '''
        Update and override any UI parameters post parent initialisation
        '''
        self.SetTitle("KCD PAK Builder (v%s) by %s" % (self._version, self._author))

        # Update Icon
        if not self.GetParent():
            icon = wx.Icon()
            icon.CopyFromBitmap(wx.Bitmap(self._get_icon_path()))
            self.SetIcon(icon)

        # ===================================================================================================
        # Process Saved Configuration
        # ===================================================================================================
        # Config: PAK Output Dir
        pak_out_dir = self._cfg.get(self.CFG_KEY_OUTPUT_DIR, "")
        if pak_out_dir is not None:
            self.dp_pak_out_dir.SetPath(pak_out_dir)
            self.cb_save_output_dir.SetValue(True)

        # Config: PAK Filename
        pak_filename = self._cfg.get(self.CFG_KEY_PAK_FILENAME, None)
        if pak_filename is not None:
            self.text_pak_filename.SetValue(pak_filename)
            self.cb_save_filename.SetValue(True)

        # Config: Target Dir
        target_dir = self._cfg.get(self.CFG_KEY_TARGET_DIR, None)
        if target_dir is not None:
            self.dp_target_dir.SetPath(target_dir)
            self.cb_save_target_dir.SetValue(True)

        # Config: Ignore Nested Paks
        self._ignore_nested_paks = self._cfg.get(self.CFG_KEY_IGNORE_NESTED_PAKS, True)
        self.cb_ignore_nested_paks.SetValue(self._ignore_nested_paks)

        # Max PAK Size
        self.text_pak_max_mb.SetValue(str(self._cfg.get(self.CFG_KEY_MAX_PAK_MB, self.DEFAULT_PAX_MAX_MB)))

        # Config: Show/Hide Options
        if self._cfg.get(self.CFG_KEY_SHOW_OPTIONS):
            self._show_options()
        else:
            self._hide_options()

    # ===================================================================================================
    # Event Callbacks/Handlers
    # ===================================================================================================
    def initiate_pack(self, pak_path, target_dir, max_size_mb=DEFAULT_PAX_MAX_MB):

        # ===================================================================================================
        # Validate Options
        # ===================================================================================================
        # Validate Max MB
        if not self._is_valid_pak_size(max_size_mb):
            self.write_to_log("Error: Maximum PAK size is invalid. Must be a number between 10 (10MB) and 51250 (50GB)")
            return

        # ===================================================================================================
        # Update UI
        # ===================================================================================================
        self.btn_stop_pak.Enable()
        self.btn_start_pak.Disable()

        # ===================================================================================================
        # Initialise PAK Builder
        # ===================================================================================================
        self._paker = PakBuilder(self, pak_path, target_dir, max_size_mb)
        self._paker.set_skip_pak_files(self.cb_ignore_nested_paks.GetValue())
        self._paker.build_filelist()
        self.pak_pg_bar.SetRange(self._paker.get_total_file_count())

        # Start Pak!
        self._paker.start_pak()

    def _on_start_pak(self, event):
        '''
        Start/Build PAK Button Callback. Called when Build PAK Button is clicked. Initiates PAK Build

        :param event: wx Click Event
        '''
        self.output_log.Clear()
        self.write_to_log("[+] Starting manual PAK Build")
        # Process Inputs
        pak_out_dir = self.dp_pak_out_dir.GetPath()
        pak_out_filename = self.text_pak_filename.GetValue()
        target_dir = self.dp_target_dir.GetPath()
        max_size_mb = self.text_pak_max_mb.GetValue()

        # ===================================================================================================
        # Validate Main Input
        # ===================================================================================================
        # Validate PAK Output Path
        if not pak_out_dir or not os.path.isdir(pak_out_dir):
            self.write_to_log("ERROR: PAK output directory is invalid or does not exist")
            return

        # Validate PAK Filename
        valid_pak_name = self._is_filename_valid(pak_out_filename)
        if not valid_pak_name:
           self.write_to_log("ERROR: Invalid PAK Filename. Should contain only letters, numbers and underscores, and must be a valid filename")
           return
        if not pak_out_filename.lower().endswith(".pak"):
            pak_out_filename += ".pak"
        pak_path = os.path.join(pak_out_dir, pak_out_filename)

        # Validate Target Directory
        if not target_dir or not os.path.isdir(target_dir):
            self.write_to_log("ERROR: Target directory is invalid or does not exist")
            return

        self.initiate_pack(pak_path, target_dir, max_size_mb)


    def _on_stop_pak(self, event):
        '''
        Stop Build Button Callback. Called when Stop button is clicked. Stops the build

        :param event: wx Event
        '''
        self._paker.stop_pak()
        self.btn_stop_pak.Disable()
        self.btn_start_pak.Enable()

    def _on_toggle_options(self, event):
        '''
        Show/Hide Options Button Callback. Called when the Show/Hide Options button is clicked

        :param event: Button Event
        :type event: wx.Event
        '''
        if self._cfg.get(self.CFG_KEY_SHOW_OPTIONS, False):
            self._hide_options()
        else:
            self._show_options()

    def _on_output_dir_change(self, event):
        '''
        Called When the PAK Output Dir path is changed

        :param event: wx Event
        '''
        if self.cb_save_output_dir.GetValue():
            output_dir = self.dp_pak_out_dir.GetPath()
            # print("Saving Output DIR: %s" % output_dir)
            self._set_config_property(self.CFG_KEY_OUTPUT_DIR, output_dir)

    def _on_target_dir_change(self, event):
        '''
        Called When the Target Dir path is changed

        :param event: wx Event
        '''
        if self.cb_save_target_dir.GetValue():
            target_dir = self.dp_target_dir.GetPath()
            # print("Saving Target DIR: %s" % target_dir)
            self._set_config_property(self.CFG_KEY_TARGET_DIR, target_dir)


    def _on_pak_max_mb_change(self, event):
        '''
        Called when the PAK Max size input changes

        :param event:
        :return:
        '''
        try:
            max_size = int(self.text_pak_max_mb.GetValue())
            self._set_config_property(self.CFG_KEY_MAX_PAK_MB, max_size)
        except ValueError:
            pass

    def _on_pak_filename_change(self, event):
        '''
        Called when the PAK Filename Text Ctrl is changed

        :param event: The change event
        :type event: wx.Event
        '''
        if self.cb_save_filename.GetValue():
            # print("Saving PAK FILENAME: %s" % self.text_pak_filename.GetValue())
            self._set_config_property(self.CFG_KEY_PAK_FILENAME, self.text_pak_filename.GetValue())

    # ===================================================================================================
    # Checkbox Callbacks
    # ===================================================================================================
    def _on_save_output_dir_cb(self, event):
        '''
        Remember Output Directory Checkbox Callback. Called when Remember Output dir checkbox is toggled

        :param event: wx Event
        '''
        save_output_dir = self.cb_save_output_dir.GetValue()
        if save_output_dir:
            self._set_config_property(self.CFG_KEY_OUTPUT_DIR, self.dp_pak_out_dir.GetPath())
        else:
            self._set_config_property(self.CFG_KEY_OUTPUT_DIR, None)

    def _on_save_filename_cb(self, event):
        '''
        Remember Filename Checkbox Callback. Called when remember filename checkbox is toggled

        :param event: The Checkbox Event
        :type event: wx.Event
        '''
        save_filename = self.cb_save_filename.GetValue()
        if save_filename:
            self._set_config_property(self.CFG_KEY_PAK_FILENAME, self.text_pak_filename.GetValue())
        else:
            self._set_config_property(self.CFG_KEY_PAK_FILENAME, None)

    def _on_save_target_dir_cb(self, event):
        '''
        Remember Target Dir Checkbox Callback. Called when remember target dir checkbox is toggled

        :param event: The Checkbox Event
        :type event: wx.Event
        '''
        save_target_dir = self.cb_save_target_dir.GetValue()
        if save_target_dir:
            self._set_config_property(self.CFG_KEY_TARGET_DIR, self.dp_target_dir.GetPath())
        else:
            self._set_config_property(self.CFG_KEY_TARGET_DIR, None)

    def _on_ignore_nested_cb(self, event):
        '''
        Ignore Nested PAKs Callback. Called when Ingore Nested PAKs checkbox is toggled

        :param event: The Checkbox Event
        :type event: wx.Event
        '''
        self._ignore_nested_paks = self.cb_ignore_nested_paks.GetValue()
        self._set_config_property(self.CFG_KEY_IGNORE_NESTED_PAKS, self._ignore_nested_paks)

    def _save_cfg(self):
        '''
        Remember directory checkbox callback.
        :param event:
        :return:
        '''
        with open(self._cfg_path, "w") as cfg_file:
            cfg_file.write(json.dumps(self._cfg))

    def _load_cfg(self):
        cfg = {}
        try:
            with open(self._cfg_path, "r") as cfg_file:
                cfg = json.loads(cfg_file.read())
        except Exception as ex:
            pass
        return cfg


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
            new_status = "%s of %s (%s%%)" % (files_processed, total_files, percent_completion)
        self.label_status.SetLabel(new_status)

        # Log file
        self.write_to_log("[+] %s" % file)

    def on_completion(self):
        '''
        Pak Completion Callback. To be called by PakBuilder when packing successfully completes
        '''
        self.btn_stop_pak.Disable()
        self.btn_start_pak.Enable()

    def write_to_log(self, msg):
        '''
        Writes a message to the Output Log

        :param msg: The message to write
        :type msg: str
        '''
        log_msg = "%s\n" % msg
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
    def _hide_options(self):
        '''
        Hides the Advanced Options Panel
        '''
        self.btn_toggle_options.SetLabel("Show Additional Options")
        self.panel_options.Hide()
        self._set_config_property(self.CFG_KEY_SHOW_OPTIONS, False)
        self.Layout()

    def _show_options(self):
        '''
        Shows the Advanced Options Panel
        '''
        self.btn_toggle_options.SetLabel("Hide Additional Options")
        self.panel_options.Show()
        self._set_config_property(self.CFG_KEY_SHOW_OPTIONS, True)
        self.Refresh()
        self.panel_options.Layout()
        self.m_panel3.Layout()
        self.MainPanel.Layout()
        self.Layout()

    def _is_filename_valid(self, filename):
        '''
        Checks if the PAK Filename is valid

        :param filename: The PAK Filename to check
        :type filename: str
        :return: True if valid, otherwise False
        :rtype: bool
        '''
        regex = re.compile("^[a-zA-Z0-9_.-]*[a-zA-Z0-9_-]$")
        if regex.match(filename):
            return True
        return False

    def _is_valid_pak_size(self, size):
        '''
        Checks that the specified PAK size in MB is a valid and acceptable size for a PAK file

        :param size: The size in MB to validate
        :type size: int
        :return: True if size is valid, otherwise False
        '''
        # Validate Max MB
        try:
            size_mb = int(size)
            if size_mb < 10 or size_mb > 51250:
                raise ValueError("Out of acceptable range")
        except ValueError as ex:
            return False
        return True

    def _get_icon_path(self):
        '''
        Gets the path to the GUI Icon (.ico) file

        :return: The path to the GUI Icon File
        :rtype: str
        '''
        icon_path = None

        if "_MEI" in __file__: # (Packed)
            icon_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "resources", "icon.ico"
            )
        else: # (Not Packed)
            icon_path = os.path.join(os.path.dirname(__file__), "resources", "icon.ico")

        return icon_path

    def _get_cfg_path(self):
        '''
        Gets the PAK Builder's cfg file path

        :return: Absolute path to the PAK Builder cfg file
        :rtype: str
        '''
        cfg_path = os.path.dirname(__file__)

        if "_MEI" in __file__: # (Packed)
            cfg_path = os.path.dirname(os.path.dirname(cfg_path))
        cfg_path = os.path.join(cfg_path, "paker.cfg")

        return cfg_path


    def _set_config_property(self, key, value, save_now=True):
        '''
        Sets and saves a configuration property

        :param key: The name of the configuration option to set
        :type key: str
        :param value: The value to set for the option
        :type value: any
        :param save_now: Whether to immediately save the updated configuration
        :type save_now: bool
        '''
        self._cfg[key] = value
        if save_now:
            self._save_cfg()


class DropTarget(wx.FileDropTarget):

    def __init__(self, gui):
        self._gui = gui
        super(DropTarget, self).__init__()
    def OnDropFiles(self, x, y, items):
        '''

        :param x:
        :param y:
        :param filenames:
        :return:
        '''
        self._gui.output_log.Clear()
        self._gui.write_to_log("[+] Processing Drag and Drop")

        # ===================================================================================================
        # Validate target
        # ===================================================================================================
        for item in items:
            if not os.path.isdir(item):
                self._gui.write_to_log("[+] Not a directory, skipping: %s" % item)
                continue
            output_dir, target_dir = os.path.split(item)
            pak_path = "%s.pak" % item

        # print("Creating %s from %s" % (pak_path, item))

            self._gui.initiate_pack(pak_path, item)
        return True
