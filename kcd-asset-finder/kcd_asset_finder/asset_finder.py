# ===================================================================================================
# Imports: External
# ===================================================================================================
import time
import os
import zipfile
import json
import re
from threading import Thread
from threading import Event
from kcd_utils import pak_utils

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
    ASSET_TYPE_ANY      = "any"
    ASSET_TYPE_MATERIAL = "material"
    ASSET_TYPE_TEXTURE  = "texture"

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
        self._search_string = ""
        self._asset_type = "any"
        self._stop_event = Event()
        self._asset_tree = {}
        super(AssetFinder, self).__init__()

    def start_search(self, search_string, asset_type):
        '''
        Starts the Asset search
        '''
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

            # Add PAK to tree
            tid_pak = tree_widget.AppendItem(tid_root, pak_name)
            if not tree_widget.IsExpanded(tid_root):
                tree_widget.Expand(tid_root)

            # Search PAK Assets
            self.search_pak_assets(pak_name, pak, tid_pak, tree_widget)

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


    def search_pak_assets(self, pak_name, pak, tid_pak, tree_widget):
        '''
        Searches the specified PAK assets for matches

        :param pak: The PAK to search
        :type pak: dict
        :return:
        '''
        # ===================================================================================================
        # Iterate PAK Assets
        # ===================================================================================================
        for asset in pak_utils.get_pak_assets(pak["abs_path"]):
            # print("ASSET: %s" % asset)
            if not self._is_matching_asset(asset.lower()):
                continue

            # ===================================================================================================
            # Iterate and Traverse Asset path
            # ===================================================================================================
            tid_parent = tid_pak
            path_sections = asset.split("/")
            for idx in range(len(path_sections)):
                path_section = path_sections[idx]                                   # e.g. humans
                current_traversal = "/".join(path_sections[:idx+1])                 # e.g. Animations/humans

                # Check if tree node already exists for current traversal
                # True: Add to tree and set that as new parent
                if current_traversal in self._asset_tree[pak_name]:
                    tid_parent = self._asset_tree[pak_name][current_traversal]
                    continue

                # False! Add current traversal to tree and THEN use THAT as parent node
                tid_parent = tree_widget.AppendItem(tid_parent, path_section)
                self._asset_tree[pak_name][current_traversal] = tid_parent

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

        :param asset: The path of the asset being checked
        :type asset: str
        :return: True if the asset matches, otherwise False
        :rtype: bool
        '''

        # ===================================================================================================
        # Asset Type Check
        # ===================================================================================================
        if self._asset_type != self.ASSET_TYPE_ANY:
            # ===================================================================================================
            # Asset - Material
            # ===================================================================================================
            if self._asset_type == self.ASSET_TYPE_MATERIAL:
                if not asset.endswith(".mtl"):
                    return False
            # ===================================================================================================
            # Asset - Texture
            # ===================================================================================================
            if self._asset_type == self.ASSET_TYPE_TEXTURE:
                if not re.match(".*\.dds(\d+)*$", asset):
                    return False

        # ===================================================================================================
        # Search String Check
        # ===================================================================================================
        if self._search_string and self._search_string not in asset:
            return False

        return True


