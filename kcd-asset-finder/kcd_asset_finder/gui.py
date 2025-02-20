# ===================================================================================================
# Imports: External
# ===================================================================================================
import os
import wx
import json
from .asset_finder import AssetFinder

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
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
        bind_target.Bind(wx.EVT_TREE_SEL_CHANGED, self._on_tree_selection_changed, self.results_tree)

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
    # Event Handlers/Callbacks
    # ===================================================================================================
    def _on_tree_selection_changed(self, event):
        print(self.results_tree.GetSelection())
        path_to_parent = []
        item = event.GetItem()
        path_to_parent.append(self.results_tree.GetItemText(item))
        parent = self.results_tree.GetItemParent(item)
        while parent.IsOk():
            path_to_parent.append(self.results_tree.GetItemText(parent))
            parent = self.results_tree.GetItemParent(parent)

        print(path_to_parent)

        print(self.results_tree.GetItemText(item))
        print(self.results_tree.GetItemParent(item))

    def _on_search(self, event):
        '''
        Search Button Callback. Called when Search button is clicked

        :param event: The Button Event
        :type event: wx.Event
        '''
        self.results_tree.DeleteAllItems()
        search_string = self.text_search.GetValue().lower()
        asset_type = self.choice_asset_type.GetStringSelection().lower()

        target_dir = "E:\\SteamLibrary\\steamapps\\common\\KingdomComeDeliverance2\\Data"
        # target_dir = "E:\\dev\\projects\\kcd-modding\\kdc2\\experimental\\asset_finder_playground"
        self._af = AssetFinder(self, target_dir)

        # ===================================================================================================
        # Update UI
        # ===================================================================================================
        self.btn_search.Disable()
        self.btn_cancel.Enable()

        self._af.start_search(search_string, asset_type)

    def _on_expand_all(self, event):
        '''
        Called when the Expand All Button is clicked

        :param event: The Button Event
        :type event: wx.Event
        '''
        self._af.set_auto_expand(True)
        self.results_tree.ExpandAll()
        self.Layout()

    def _on_collapse_all(self, event):
        '''
        Called when the Collapse All Button is clicked

        :param event: The Button Event
        :type event: wx.Event
        '''
        self._af.set_auto_expand(False)
        tid_root = self.results_tree.GetRootItem()
        child_ref, child_cookie = self.results_tree.GetFirstChild(tid_root)
        while child_ref.IsOk():
            self.results_tree.Collapse(child_ref)
            child_ref, child_cookie = self.results_tree.GetNextChild(tid_root, child_cookie)
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
        self._match_count += 1
        self.label_matches.SetLabel("%s match(es)" % self._match_count)
        self.Layout()

    def on_pak_processed(self, pak):
        '''
        Called when a PAK file is successfully processed

        :param pak: The PAK that was successfully processed
        :type pak: str
        '''
        pak_idx = list(self._paks.keys()).index(pak)
        self.pb_search.SetValue(pak_idx)

        # Calculate Progress Percentage
        progress_percent = int(pak_idx / (len(self._paks) - 1) * 100)
        self.label_percentage.SetLabel("%s%%" % progress_percent)

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
            self.results_tree.AppendItem(pak, path)


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