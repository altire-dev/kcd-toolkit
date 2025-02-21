# ===================================================================================================
# Imports: External
# ===================================================================================================
import os
import wx
import json
from kcd_utils import utils
from kcd_utils import pak_utils

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .asset_finder import AssetFinder
from .abs_gui import MainFrame

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

        bind_target.Bind(wx.EVT_BUTTON, self._on_search, self.btn_search)
        bind_target.Bind(wx.EVT_BUTTON, self._on_cancel, self.btn_cancel)
        bind_target.Bind(wx.EVT_BUTTON, self._on_expand_all, self.btn_expand_all)
        bind_target.Bind(wx.EVT_BUTTON, self._on_collapse_all, self.btn_collapse_all)
        bind_target.Bind(wx.EVT_BUTTON, self._on_export, self.btn_export)
        bind_target.Bind(wx.EVT_TREE_SEL_CHANGED, self._on_tree_selection_changed, self.tree_widget)

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

            # Auto Detect KCD2 path
            kcd2_path = utils.find_kcd2_path()
            self.dp_kcd2_path.SetPath(kcd2_path)

    # ===================================================================================================
    # Event Handlers/Callbacks
    # ===================================================================================================
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

        # ===================================================================================================
        # Validate Input
        # ===================================================================================================
        if not os.path.isdir(export_path):
            self.label_status.SetLabel("Error: Export Path does not exist")
            return

        # ===================================================================================================
        # Export!
        # ===================================================================================================
        for pak, asset  in self._selected_items:
            pak_path = os.path.join(self.dp_kcd2_path.GetPath(), "Data", pak)
            pak_utils.export_pak_asset(export_path, pak_path, asset)


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
            pak, asset_path = self._build_item_asset_path(selected_node)
            if pak and asset_path:
                self._selected_items.append((pak, asset_path))
                path_sections = asset_path.split("/")
                if not path_sections or not "." in path_sections[-1]:
                    can_export = False
            else:
                can_export = False

        # ===================================================================================================
        # Update Export Button state
        # ===================================================================================================
        if can_export:
            self.btn_export.Enable()
            self.dp_export_path.Enable()
        else:
            self.btn_export.Disable()
            self.dp_export_path.Disable()

    def _on_search(self, event):
        '''
        Search Button Callback. Called when Search button is clicked

        :param event: The Button Event
        :type event: wx.Event
        '''

        # ===================================================================================================
        # Process User Input
        # ===================================================================================================
        search_string   = self.text_search.GetValue().lower()
        asset_type      = self.choice_asset_type.GetStringSelection().lower()
        kcd2_path       = self.dp_kcd2_path.GetPath()

        # ===================================================================================================
        # Validate Input
        # ===================================================================================================
        if not os.path.isdir(kcd2_path):
            self.label_status.SetLabel("Error: KCD2 Path Does not exist")
            return
        target_dir = os.path.join(kcd2_path, "Data")
        if not os.path.isdir(target_dir):
            self.label_status.SetLabel("Error: Invalid KCD2 Path. Data directory not found")
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
        self._af.start_search(search_string, asset_type)

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
        # self.Layout()

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

    def _build_item_asset_path(self, item):
        '''
        Builds the absolute PAK path to an asset from a tree node item

        :param item: The Tree Item that was selected
        :type item: wx.TreeItemId
        :return: Asset PAK, and complete path for the node item inside PAK
        :rtype: tuple
        '''
        pak = None
        asset_location = None
        tree_path = []
        item_label = self.tree_widget.GetItemText(item)

        parent = self.tree_widget.GetItemParent(item)
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
            pak = tree_path[-1]
            asset_location = "/".join(
                list(reversed(tree_path[:-1])) + [item_label]
            )

        print("Asset Location: %s" % asset_location)

        return pak, asset_location
