# ===================================================================================================
# Imports: External
# ===================================================================================================
import os
import wx
import json
from kcd_core.utils import sys_utils
from kcd_core.utils import pak_utils

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .asset_finder import AssetFinder
from .abs_gui import MainFrame
from .abs_gui import MessageDialog

# ===================================================================================================
# KCD Mod Generator GUI Class
# ===================================================================================================
class KCDAssetFinderGui(MainFrame):
    '''
    KCD Asset Finder GUI
    '''

    # ===================================================================================================
    # Properties
    # ===================================================================================================
    ROOT_NODE_LABEL = "PAKs"

    CFG_KEY_KCD2_PATH       = "kcd2_path"
    CFG_KEY_EXPORT_PATH     = "export_path"
    CFG_KEY_PRESERVE_PATHS  = "preserve_export_paths"

    # ===================================================================================================
    # Class Functions
    # ===================================================================================================

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
        self._mod_folder_path = None
        self._af = None
        self._match_count = 0
        self._paks = {}
        self._tids = {}
        self._pak_tree = {}
        self._selected_items = []

        # Load Configuration
        self._cfg_path = self._get_cfg_path()
        self._cfg = self._load_cfg()

        # Initialise Frame
        super(KCDAssetFinderGui, self).__init__(suite)

        # Set Up GUI
        self._bind_events()
        self._init_ui()

    def _bind_events(self):
        '''
        Binds GUI Events
        '''
        bind_target = self
        if self.GetParent():
            bind_target = self.GetParent()

        # ===================================================================================================
        # Button Events
        # ===================================================================================================
        bind_target.Bind(wx.EVT_BUTTON, self._on_search, self.btn_search)
        bind_target.Bind(wx.EVT_BUTTON, self._on_cancel, self.btn_cancel)
        bind_target.Bind(wx.EVT_BUTTON, self._on_expand_all, self.btn_expand_all)
        bind_target.Bind(wx.EVT_BUTTON, self._on_collapse_all, self.btn_collapse_all)
        bind_target.Bind(wx.EVT_BUTTON, self._on_export, self.btn_export)

        # ===================================================================================================
        # Input Change Events
        # ===================================================================================================
        bind_target.Bind(wx.EVT_DIRPICKER_CHANGED, self._on_kcd2_path_change, self.dp_kcd2_path)
        bind_target.Bind(wx.EVT_DIRPICKER_CHANGED, self._on_export_path_change, self.dp_export_path)
        bind_target.Bind(wx.EVT_CHECKBOX, self._on_preserve_paths_change, self.checkbox_preserve_paths)

        # ===================================================================================================
        # Misc Events
        # ===================================================================================================
        bind_target.Bind(wx.EVT_TEXT_ENTER, self._on_search, self.text_search)
        bind_target.Bind(wx.EVT_TREE_SEL_CHANGED, self._on_tree_selection_changed, self.tree_widget)
        bind_target.Bind(wx.EVT_CLOSE, self._on_close, self)

    def _init_ui(self):
        '''
        Updates and set ups the UI
        '''
        self.SetTitle("KCD Asset Finder (v%s) by %s" % (self._version, self._author))

        # Update Icon
        if not self.GetParent():
            icon = wx.Icon()
            icon.CopyFromBitmap(wx.Bitmap(self._get_icon_path()))
            self.SetIcon(icon)

        # ===================================================================================================
        # Process Saved Configuration
        # ===================================================================================================
        # Config: KCD2 Path
        kcd2_path = self._cfg.get(self.CFG_KEY_KCD2_PATH, "")
        if not kcd2_path:
            # Attempt auto-detection
            kcd2_path = sys_utils.find_kcd2_path()
        kcd2_path = str(kcd2_path)
        if kcd2_path:
            self.dp_kcd2_path.SetPath(kcd2_path)

        # Config: Export Path
        export_path = self._cfg.get(self.CFG_KEY_EXPORT_PATH, "")
        str(export_path)
        self.dp_export_path.SetPath(export_path)

        # Config: Preservce Export Paths
        preserve_paths = self._cfg.get(self.CFG_KEY_PRESERVE_PATHS, False)
        self.checkbox_preserve_paths.SetValue(preserve_paths)

    # ===================================================================================================
    # Event Handlers/Callbacks
    # ===================================================================================================
    def _on_preserve_paths_change(self, event):
        '''
        Called when the "Preserve Paths" checkbox state is changed

        :param event: The Checkbox Event
        :type event: wx.Event
        '''
        preserve_paths = self.checkbox_preserve_paths.GetValue()
        self._set_config_property(self.CFG_KEY_PRESERVE_PATHS, preserve_paths)

    def _on_kcd2_path_change(self, event):
        '''
        Called when the KCD2 Path is changed

        :param event: wx Event
        '''
        kcd2_path = self.dp_kcd2_path.GetPath()
        self._set_config_property(self.CFG_KEY_KCD2_PATH, kcd2_path)

    def _on_export_path_change(self, event):
        '''
        Called when the Export Path is changed

        :param event: wx Event
        '''
        export_path = self.dp_export_path.GetPath()
        self._set_config_property(self.CFG_KEY_EXPORT_PATH, export_path)

    def _on_close(self, event):
        '''
        Application Close Callback. Called when application is closed by the user. Gracefully terminates Asset Finder
        '''
        if self._af:
            self._af.stop_search()
        self.Destroy()

    def _on_export(self, event):
        '''
        The Export Selected Button Callback. Called when the Export Selected button is clicked

        :param event: The button event
        :type event: wx.Event
        '''
        # ===================================================================================================
        # Process Input
        # ===================================================================================================
        export_path = self.dp_export_path.GetPath()
        preserve_paths  = self.checkbox_preserve_paths.GetValue()

        # ===================================================================================================
        # Validate Input
        # ===================================================================================================
        if not os.path.isdir(export_path):
            self._display_message("Error", "Export directory not set or does not exist")
            return

        # ===================================================================================================
        # Export!
        # ===================================================================================================
        for pak, asset  in self._selected_items:
            if preserve_paths:
                export_path = os.path.join(export_path, asset.get_dir()).replace("/", "\\")
            pak.export_asset(asset, export_path)

        self._display_message(
            "Export Complete",
            "%s asset(s) successfully exported" % len(self._selected_items)
        )


    def _on_test(self, event):
        export_dialog = MessageBox(self)
        export_dialog.set_message("Wooop" * 10)
        self.Disable()
        export_dialog.Show()


    def _on_tree_selection_changed(self, event):
        '''
        Tree Selection Changed Callback. Called when the selection in the tree control is changed
        :param event:
        :return:
        '''
        can_export = True
        self._selected_items.clear()

        # ===================================================================================================
        # Converted Selected Nodes into Asset Items
        # ===================================================================================================
        selected_nodes = self.tree_widget.GetSelections()
        for selected_node in selected_nodes:
            pak, asset = self._resolve_node_to_asset(selected_node)
            if pak and asset:
                self._selected_items.append((pak, asset))
            else:
                can_export = False

        # ===================================================================================================
        # Update Export Button state
        # ===================================================================================================
        if can_export:
            self.btn_export.Enable()
            self.dp_export_path.Enable()
            self.checkbox_preserve_paths.Enable()
        else:
            self.btn_export.Disable()
            self.dp_export_path.Disable()
            self.checkbox_preserve_paths.Disable()

    def _on_search(self, event):
        '''
        Search Button Callback. Called when Search button is clicked

        :param event: The Button Event
        :type event: wx.Event
        '''

        # ===================================================================================================
        # Update UI
        # ===================================================================================================
        self.btn_export.Disable()
        self.dp_export_path.Disable()
        self.checkbox_preserve_paths.Disable()

        # ===================================================================================================
        # Process User Input
        # ===================================================================================================
        search_type     = self.choice_search_type.GetCurrentSelection()
        search_string   = self.text_search.GetValue().lower()
        asset_type      = self.choice_asset_type.GetCurrentSelection()
        kcd2_path       = self.dp_kcd2_path.GetPath()

        # ===================================================================================================
        # Validate Input
        # ===================================================================================================
        if not kcd2_path:
            self._display_message("Error", "KCD2 Installation Path must be set")
            return
        if not os.path.isdir(kcd2_path):
            self._display_message("Error", "The KCD2 Path Does not exist")
            return
        target_dir = os.path.join(kcd2_path, "Data")
        if not os.path.isdir(target_dir):
            self._display_message("Error", "Invalid KCD2 Path. Data directory not found")
            return

        # ===================================================================================================
        # Update UI
        # ===================================================================================================
        self.btn_search.Disable()
        self.btn_cancel.Enable()

        # ===================================================================================================
        # Set Up Tree
        # ===================================================================================================
        self.tree_widget.DeleteAllItems()
        tid_root = self.tree_widget.AddRoot(self.ROOT_NODE_LABEL)
        self.tree_widget.Expand(tid_root)

        # ===================================================================================================
        # Initiate Search
        # ===================================================================================================
        self._af = AssetFinder(self, target_dir)
        self._af.start_search(search_type, search_string, asset_type)

    def _on_expand_all(self, event):
        '''
        Called when the Expand All Button is clicked

        :param event: The Button Event
        :type event: wx.Event
        '''
        self.tree_widget.ExpandAll()
        self.Layout()

    def _on_collapse_all(self, event):
        '''
        Called when the Collapse All Button is clicked

        :param event: The Button Event
        :type event: wx.Event
        '''
        tid_root = self.tree_widget.GetRootItem()
        if tid_root.IsOk():
            child_ref, child_cookie = self.tree_widget.GetFirstChild(tid_root)
            while child_ref.IsOk():
                self.tree_widget.Collapse(child_ref)
                child_ref, child_cookie = self.tree_widget.GetNextChild(tid_root, child_cookie)
            self.Layout()

    def _on_cancel(self, event):
        '''
        Cancel Button Callback. Called when the Cancel button is clicked

        :param event: The Button event
        :type event: wx.Event
        '''
        self.label_status.SetLabel("Cancelling")
        self._af.stop_search()
        self.pb_search.SetValue(0)

    def on_search_success(self):
        '''
        Search Finished Successfully Callback. Called when the search successfully finishes
        '''
        self.btn_search.Enable()
        self.btn_cancel.Disable()
        self.label_status.SetLabel("Search Complete")

    def on_search_cancelled(self):
        '''
        Search Cancelled Callback. Called if the search is cancelled
        '''
        self.btn_search.Enable()
        self.btn_cancel.Disable()
        self.label_status.SetLabel("Cancelled")

    def on_match_found(self):
        '''
        Called when a new match is found
        '''
        pass

    def on_pak_processed(self, pak):
        '''
        Called when a PAK file is successfully processed

        :param pak: The PAK that was successfully processed
        :type pak: str
        '''
        # Update Search Status
        pak_idx = list(self._paks.keys()).index(pak)
        self.pb_search.SetValue(pak_idx)

        # Update Search Percentage
        progress_percent = int(pak_idx / (len(self._paks) - 1) * 100)
        self.label_percentage.SetLabel("%s%%" % progress_percent)
        self.Layout()

    def on_processing_pak(self, pak):
        '''
        Called when AssetFinder begins to process a PAK

        :param pak: The PAK that AssetFinder is starting to process
        :type pak: str
        '''
        self.label_status.SetLabel("Processing %s" % pak)

    def on_match_found(self, pak, asset):
        '''
        Asset match callback. Called when a matching asset is found

        :param asset: The matching asset
        :type asset: str
        '''

        for path in asset.split("/"):
            self.tree_widget.AppendItem(pak, path)


    # ===================================================================================================
    # Getters
    # ===================================================================================================
    def get_tree(self):
        '''
        Gets the results tree widget

        :return: The Results Tree widget instance
        :rtype: wx.TreeCtrl
        '''
        return self.tree_widget

    # ===================================================================================================
    # Setters
    # ===================================================================================================
    def set_paks(self, paks):
        '''
        Sets the inventory of discovered PAKs

        :param paks: The PAK inventory
        :type paks: dict
        '''
        self._paks = paks
        self.pb_search.SetRange(len(self._paks) - 1)

    # ===================================================================================================
    # Internal/Helper Methods
    # ===================================================================================================
    def _display_message(self, title, message):
        '''
        Displays an info message to the user

        :param title: The title of the info message
        :type title: str
        :param message: The contents of the info message
        :type message: str
        '''
        export_dialog = MessageBox(self)
        export_dialog.set_title(title)
        export_dialog.set_message(message)

        self.Disable()
        export_dialog.Show()

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

    def _resolve_node_to_asset(self, node):
        '''
        Builds the absolute PAK path to an asset from a tree node item

        :param node: The Tree node that was selected
        :type node: wx.TreeItemId
        :return: PAKFile and PAKAsset for target node
        :rtype: tuple(PAKFile, PAKAsset)
        '''
        pak = None
        asset_location = None
        asset = None
        tree_path = []
        node_label = self.tree_widget.GetItemText(node)

        parent = self.tree_widget.GetItemParent(node)
        while parent.IsOk():
            parent_label = self.tree_widget.GetItemText(parent)
            if parent_label == self.ROOT_NODE_LABEL:
                break
            tree_path.append(parent_label)
            parent = self.tree_widget.GetItemParent(parent)


        # ===================================================================================================
        # Rebuild Path
        # ===================================================================================================
        if len(tree_path) > 0:
            pak_name = tree_path[-1]
            pak = self._paks[pak_name]
            asset_location = "/".join(
                list(reversed(tree_path[:-1])) + [node_label]
            )

        if pak:
            asset = pak.get_asset_by_path(asset_location)

        return pak, asset

    def _get_cfg_path(self):
        '''
        Gets the Asset Finder's cfg file path

        :return: Absolute path to the Asset Finder cfg file
        :rtype: str
        '''
        cfg_path = os.path.dirname(__file__)

        if "_MEI" in __file__: # (Packed)
            cfg_path = os.path.dirname(os.path.dirname(cfg_path))
        cfg_path = os.path.join(cfg_path, "assetfinder.cfg")

        return cfg_path

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


# ===================================================================================================
# Message Dialog Class
# ===================================================================================================
class MessageBox(MessageDialog):
    '''
    Message Box for displaying Messages to the user
    '''

    # ===================================================================================================
    # Methods
    # ===================================================================================================
    def __init__(self, parent):
        '''
        Constructor
        '''
        super(MessageBox, self).__init__(parent)
        self._bind_events()

    def _bind_events(self):
        '''
        Binds events for the Message Box
        '''
        self.Bind(wx.EVT_BUTTON, self._on_ok, self.btn_ok)
        self.Bind(wx.EVT_CLOSE, self._on_ok, self)

    # ===================================================================================================
    # Event Handlers/Callbacks
    # ===================================================================================================
    def _on_ok(self, event):
        '''
        OK Button Callback Handler. Called when the OK button is clicked

        :param event: The Button event
        :type event: wx.Event
        '''
        self.GetParent().Enable()
        self.Destroy()


    # ===================================================================================================
    # Setters
    # ===================================================================================================
    def set_title(self, title):
        '''
        Sets the Message Box's title text

        :param title: The new title
        :type title: str
        '''
        self.SetTitle(title)

    def set_message(self, message):
        '''
        Sets the Message Box's message text

        :param message: The message to display
        :type message: str
        '''
        self.dialog_text.SetLabel(message)
