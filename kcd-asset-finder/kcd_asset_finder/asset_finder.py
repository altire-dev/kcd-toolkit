# ===================================================================================================
# Imports: External
# ===================================================================================================
import re
from threading import Thread
from threading import Event

import wx

from kcd_core.utils import pak_utils
from kcd_core.components.pak import PAKFile
from kcd_core.components.pak import PAKAsset
from kcd_core.components.pak.pak_asset_types import *

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
# from . import KCDAssetFinderGui


# ===================================================================================================
# Asset Finder Class
# ===================================================================================================
class AssetFinder(Thread):
    '''
    KCD Asset Finder
    '''

    # ===================================================================================================
    # Properties
    # ===================================================================================================
    SEARCH_TYPE_CONTAINS        = 0
    SEARCH_TYPE_NOT_CONTAINS    = 1
    SEARCH_TYPE_REGEX           = 2

    # ===================================================================================================
    # Methods
    # ===================================================================================================
    def __init__(self, gui, target_dir):
        '''
        constructor

        :param gui: The parent KCD Asset Finder GUI Instance
        :type gui: KCDAssetFinderGui
        :param target_dir: The Target Directory to search
        :type target_dir: Absolute path to the target directory to search
        '''
        self._target_dir = target_dir
        self._gui = gui
        self._search_type = self.SEARCH_TYPE_CONTAINS
        self._search_string = ""
        self._asset_type = ASSET_ANY
        self._stop_event = Event()
        self._asset_tree = {}
        super(AssetFinder, self).__init__()

    def start_search(self, search_type, search_string, asset_type):
        '''
        Starts the Asset search

        :param search_type: The type of Search to run
        :type search_type: int
        '''
        self._search_type = search_type
        self._search_string = search_string
        self._asset_type = asset_type
        self.start()

    def stop_search(self):
        '''
        Stops the Asset search
        '''
        self._stop_event.set()

    def run(self):
        '''
        Thread Runner. Performs the search
        :return:
        '''
        self._asset_tree = {}

        # ===================================================================================================
        # Run PAK Discovery
        # ===================================================================================================
        paks = pak_utils.find_paks(self._target_dir)
        self._gui.set_paks(paks)

        # ===================================================================================================
        # Search PAK Files
        # ===================================================================================================
        self.search_paks(paks)

    def search_paks(self, paks):
        '''
        Searches the provided PAK Files

        :param paks: A List of PAK Files to search
        :type paks: dict
        '''
        tree_widget = self._gui.get_tree()
        tid_root = tree_widget.GetRootItem()

        # ===================================================================================================
        # Iterate PAKs
        # ===================================================================================================
        for pak_name, pak in paks.items():
            self._asset_tree[pak_name] = {}
            self._gui.on_processing_pak(pak_name)

            # Search PAK Assets
            matching_assets = self.search_pak_assets(pak)
            if matching_assets:
                # Add PAK to tree
                tid_pak = tree_widget.AppendItem(tid_root, pak_name)
                if not tree_widget.IsExpanded(tid_root):
                    tree_widget.Expand(tid_root)
                self._build_pak_tree(pak, tid_pak, tree_widget, matching_assets)

            # Check for Interrupt
            if self.was_stopped():
                self._gui.on_search_cancelled()
                break

            self._gui.on_pak_processed(pak_name)

        # ===================================================================================================
        # Success - Search Finished
        # ===================================================================================================
        if not self.was_stopped():
            self._gui.on_search_success()

    def search_pak_assets(self, pak):
        '''
        Searches the specified PAK assets for matches

        :param pak: The PAK to search
        :type pak: PAKFile
        :return:
        '''
        matching_assets = []
        # ==================================================================================================
        # Iterate PAK Assets
        # ===================================================================================================
        for asset in pak.get_assets():
            if self._is_matching_asset(asset):
                matching_assets.append(asset)
        return matching_assets

    def _build_pak_tree(self, pak, tid_pak, tree_widget, assets):
        '''
        Builds the Asset Tree for the PAK File

        :param pak: The PAK file to build the asset tree for
        :type pak: PAKFile
        :param tid_pak: The Table Node ID for the PAK File
        :type tid_pak: str
        :param tree_widget: The wxTreeCtrl for the results
        :type tree_widget: wxTreeCtrl
        :param assets: The PAK File assets
        :type assets: list[PAKAsset]
        :return:
        '''

        # ===================================================================================================
        # Add PAK Assets to Tree
        # ===================================================================================================
        for asset in assets:
            # ===================================================================================================
            # Iterate and Traverse Asset path
            # ===================================================================================================
            path_sections = asset.get_path_sections()
            tid_parent = tid_pak
            for idx in range(len(path_sections)):
                path_section = path_sections[idx]                                   # e.g. humans
                current_traversal = "/".join(path_sections[:idx+1])                 # e.g. Animations/humans

                # Check if tree node already exists for current traversal
                # True: Add to tree and set that as new parent
                if current_traversal in self._asset_tree[pak.get_name()]:
                    tid_parent = self._asset_tree[pak.get_name()][current_traversal]
                    continue

                # False! Add current traversal to tree and THEN use THAT as parent node
                tid_parent = tree_widget.AppendItem(tid_parent, path_section)
                self._asset_tree[pak.get_name()][current_traversal] = tid_parent

            # Check for Interrupt
            if self.was_stopped():
                break

    # ===================================================================================================
    # Getters
    # ===================================================================================================
    def was_stopped(self):
        '''
        Checks if the Thread was stopped/halted

        :return: True if build was cancelled, otherwise False
        :rtype: bool
        '''
        return self._stop_event.is_set()


    # ===================================================================================================
    # Internal Functions
    # ===================================================================================================
    def _is_matching_asset(self, asset):
        '''
        Checks if the target asset matches the current search

        :param asset: The PAKAsset being checked
        :type asset: PAKAsset
        :return: True if the asset matches, otherwise False
        :rtype: bool
        '''

        # ===================================================================================================
        # Match Asset Type
        # ===================================================================================================
        if self._asset_type != ASSET_ANY and not asset.is_of_type(self._asset_type):
            return False

        # ===================================================================================================
        # Process Search Types
        # ===================================================================================================
        if self._search_string:
            if self._search_type == self.SEARCH_TYPE_CONTAINS:
                if self._search_string not in asset.get_filename():
                    return False
            elif self._search_type == self.SEARCH_TYPE_NOT_CONTAINS:
                if self._search_string in asset.get_filename():
                    return False
            elif self._search_type == self.SEARCH_TYPE_REGEX:
                if not re.match(self._search_string, asset.get_filename()):
                    return False

        return True


