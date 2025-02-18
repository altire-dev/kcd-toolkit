# ===================================================================================================
# Imports: External
# ===================================================================================================
import os
import wx
import json
import re

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .abs_gui import MainFrame
from .manifest import ModManifest
from . import utils

# ===================================================================================================
# KCD Mod Generator GUI Class
# ===================================================================================================
class KCDModGeneratorGui(MainFrame):
    '''
    KCD Mod Generator GUI
    '''

    # ===================================================================================================
    # Properties
    # ===================================================================================================
    CFG_KEY_KCD2_PATH   = "kcd2_path"
    CFG_KEY_AUTHOR_NAME = "author"

    # ===================================================================================================
    # Methods
    # ===================================================================================================
    def __init__(self, version, author):
        '''
        Constructor

        :param version: The app version
        :type version: str
        :param author: The app author
        :type author: str
        '''
        self._version = version
        self._author = author
        self._mod_folder_path = None

        # Initialise Frame
        super(KCDModGeneratorGui, self).__init__(None)

        # Load Configuration
        self._cfg_path = self._get_cfg_path()
        self._cfg = self._load_cfg()
        if not self._cfg.get(self.CFG_KEY_KCD2_PATH):
            kcd2_path = utils.find_kcd2_path()
            self._cfg[self.CFG_KEY_KCD2_PATH] = kcd2_path
            if kcd2_path:
                self.write_to_log("KCD2 path auto-detected: %s" % kcd2_path)
        self._save_cfg()

        # Set Up GUI
        self._bind_events()
        self._init_ui()

    def _bind_events(self):
        '''
        Binds GUI Events
        '''

        # Button Events
        self.Bind(wx.EVT_BUTTON, self._on_generate_mod, self.btn_generate_mod)
        self.Bind(wx.EVT_BUTTON, self._on_open_mod_folder, self.btn_open_folder)

        # Change Events
        self.Bind(wx.EVT_DIRPICKER_CHANGED, self._on_kcd2_path_change, self.dp_kcd2_path)
        self.Bind(wx.EVT_TEXT, self._on_author_change, self.text_mod_author)

    def _init_ui(self):
        '''
        Updates and set ups the UI
        '''
        self.SetTitle("KCD Mod Generator (v%s) by %s" % (self._version, self._author))

        # Update Icon
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(self._get_icon_path()))
        self.SetIcon(icon)

        # ===================================================================================================
        # Process Configuration
        # ===================================================================================================
        self.dp_kcd2_path.SetPath(str(self._cfg.get(self.CFG_KEY_KCD2_PATH, "")))
        self.text_mod_author.SetValue(self._cfg.get(self.CFG_KEY_AUTHOR_NAME, ""))

    # ===================================================================================================
    # Event Callbacks/Handlers
    # ===================================================================================================
    def _on_generate_mod(self, event):
        '''
        Generate Mod Button Callback. Called when the Generate Mod button is clicked

        :param event: The Button Event
        :type: wx.Event
        '''
        self.text_output_log.Clear()
        self.pg_bar.SetValue(0)

        # ===================================================================================================
        # Process Inputs
        # ===================================================================================================
        kcd2_path       = self.dp_kcd2_path.GetPath()
        id              = self.text_mod_id.GetValue()
        name            = self.text_mod_name.GetValue()
        author          = self.text_mod_author.GetValue()
        version         = self.text_mod_version.GetValue()
        kcd2_version    = self.text_kcd2_version.GetValue()
        desc            = self.text_mod_desc.GetValue()

        # ===================================================================================================
        # Validate Input
        # ===================================================================================================
        if not os.path.isdir(kcd2_path):
            self.write_to_log("Error: KCD2 Installation path is invalid or does not exist", True)
            return
        if not self._is_valid_id(id):
            self.write_to_log("Error: Mod ID must be set, and should only contain letters, numbers, underscores and hyphens.")
            return
        if not name:
            self.write_to_log("Error: Mod Name must be set")
            return
        if not author:
            self.write_to_log("Error: Mod Author must be set")
            return
        if not version:
            self.write_to_log("Error: Mod Version must be set")
            return
        if not desc:
            self.write_to_log("Error: Mod Description must be set")
            return


        # ===================================================================================================
        # Build Paths
        # ===================================================================================================
        mods_path           = os.path.join(kcd2_path, "mods")
        mod_path            = os.path.join(mods_path, id)
        data_path           = os.path.join(mod_path, "Data")
        localization_path   = os.path.join(mod_path, "Localization")
        manifest_path = os.path.join(mod_path, "mod.manifest")

        if not os.path.isdir(mods_path):
            self.write_to_log("Creating 'mods' folder")
            os.mkdir(mods_path)
        if os.path.isdir(mod_path):
            self.write_to_log("Error: A mod with the id '%s' already exists" % id)
            return

        # ===================================================================================================
        # Build Mod file structure
        # ===================================================================================================
        os.mkdir(mod_path)
        os.mkdir(data_path)
        os.mkdir(localization_path)

        # ===================================================================================================
        # Apply EULA
        # ===================================================================================================
        self._copy_eula(mod_path)

        # ===================================================================================================
        # Write Manifest
        # ===================================================================================================
        manifest = ModManifest(id, name,author, version, kcd2_version, desc)
        manifest.write_to(manifest_path)

        # ===================================================================================================
        # Success!
        # ===================================================================================================
        self.pg_bar.SetValue(100)
        self._set_mod_folder_path(mod_path)
        self.write_to_log("Mod successfully generated!")

    def _on_kcd2_path_change(self, event):
        '''
        KCD2 Installation Path Change Callback. Called when the value in the KCD2 Installation Path Input is changed

        :param event: The change event
        :return: wx.Event
        '''
        kcd2_path = self.dp_kcd2_path.GetPath()
        self._cfg[self.CFG_KEY_KCD2_PATH] = kcd2_path
        self._save_cfg()

    def _on_author_change(self, event):
        '''
        Mod Author Name Change Callback. Called when the Mod Author property is changed

        :param event: The change event
        :return: wx.Event
        '''
        author = self.text_mod_author.GetValue()
        self._cfg[self.CFG_KEY_AUTHOR_NAME] = author
        self._save_cfg()

    def _on_open_mod_folder(self, event):
        '''
        Open Mod Folder Button Click Callback. Called when the "Open Mod Folder" Button is clicked

        :param event: The Button Event
        :type event: wx.Event
        '''
        utils.open_explorer_path(self._mod_folder_path)


    # ===================================================================================================
    # Internal/Helper Methods
    # ===================================================================================================
    def write_to_log(self, msg, error=False):
        '''
        Writes the specific message to the output log window

        :param msg: The message to write
        :type msg: str
        :param: Whether the message is an error
        :type error: boold
        '''
        status_char = "+"
        if error:
            status_char = "!!"

        message = "[%s] %s\n" % (status_char, msg)
        self.text_output_log.write(message)

    def _set_mod_folder_path(self, path):
        '''
        Sets the path for the "Open Mod Folder" button

        :param path: The poth to go to when the button is clicked
        :type path: str
        '''
        self._mod_folder_path = path
        self.btn_open_folder.Enable()

    def _load_cfg(self):
        cfg = {}
        try:
            with open(self._cfg_path, "r") as cfg_file:
                cfg = json.loads(cfg_file.read())
            self.write_to_log("Config file loaded from %s" % self._cfg_path)
        except Exception as ex:
            pass
        return cfg

    def _save_cfg(self):
        '''
        :param event:
        :return:
        '''
        with open(self._cfg_path, "w") as cfg_file:
            cfg_file.write(json.dumps(self._cfg))

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
        Gets the cfg file path

        :return: Absolute path to the cfg file
        :rtype: str
        '''
        cfg_path = os.path.dirname(__file__)

        if "_MEI" in __file__: # (Packed)
            cfg_path = os.path.dirname(os.path.dirname(cfg_path))
        cfg_path = os.path.join(cfg_path, "modgenerator.cfg")

        return cfg_path

    def _get_eula_path(self):
        '''
        Gets the path to the modding EULA

        :return: The absolute path to the modding EULA
        :rtype: str
        '''

        if "_MEI" in __file__: # (Packed)
            eula_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "resources", "modding_eula.txt"
            )
        else: # (Not Packed)
            eula_path = os.path.join(os.path.dirname(__file__), "resources", "modding_eula.txt")

        return eula_path

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

    def _copy_eula(self, target_dir):
        '''
        Copies and applies the modding EULA to the specified directory

        :param target_dir: Path to the directory to apply the modding EULA
        :type target_dir: str
        '''
        # Read EULA contents
        eula_src_path = self._get_eula_path()
        print("Path is: %s" % eula_src_path)
        with open(eula_src_path, "rb") as eula_src:
            eula_contents = eula_src.read()

        # Write Mod EULA
        target_path = os.path.join(target_dir, "modding_eula.txt")
        with open(target_path, "wb") as eula_file:
            eula_file.write(eula_contents)

    # ===================================================================================================
    # Validators
    # ===================================================================================================
    def _is_valid_id(self, id):
        '''
        Checks if the provided Mod ID string is valid

        :param id: The Mod ID to validate
        :type id: str
        :return: True if the ID is valid, otherwise False
        :rtype: bool
        '''
        regex = re.compile("^[a-zA-Z0-9_-]+$")
        if regex.match(id):
            return True
        return False
