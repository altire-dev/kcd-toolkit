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
        self._auto_expand = False
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
        results_tree = self._gui.results_tree
        limit = 40
        counter = 0

        # ===================================================================================================
        # Run PAK Discovery
        # ===================================================================================================
        paks = pak_utils.find_paks(self._target_dir)
        self._gui.set_paks(paks)

        # Tree Node Tests
        tid_root = results_tree.AddRoot("PAKs")
        for pak_name, pak in paks.items():
            tree = {}
            has_been_collapsed = False
            # time.sleep(2)
            self._gui.on_processing_pak(pak_name)

            if not results_tree.IsExpanded(tid_root):
                results_tree.Expand(tid_root)
            tid_pak = results_tree.AppendItem(tid_root, pak_name)
            for asset in pak_utils.get_pak_file_list(pak["abs_path"]):
                print("ASSET: %s" % asset)
                if self._is_matching_asset(asset.lower()):

                    # ===================================================================================================
                    # Splitting Test Start
                    # ===================================================================================================
                    # self._gui.on_match_found(tid_pak, asset)
                    parent = tid_pak
                    path_sections = asset.split("/")
                    for idx in range(len(path_sections)):
                        path_section = path_sections[idx]
                        abs_path = "/".join(path_sections[:idx+1])
                        print(abs_path)
                        if abs_path not in tree:
                            print("Abs Path not in tree: %s" % abs_path)
                            print("Adding item: %s" % path_section)
                            parent = results_tree.AppendItem(parent, path_section)
                            tree[abs_path] = parent
                        else:
                            parent = tree[abs_path]

                    # for path_section in asset.split("/"):
                    #     print(path_section)
                    #     parent = results_tree.AppendItem(parent, path_section)

                    # if asset not in tree:
                    #     tid_item = results_tree.AppendItem(tid_pak, asset)

                    # ===================================================================================================
                    # Splitting Test End
                    # tid_item = results_tree.AppendItem(tid_pak, asset)

                    if self._auto_expand:
                        if not results_tree.IsExpanded(tid_pak):
                            results_tree.ExpandAllChildren(tid_pak)
                    else:
                        if not has_been_collapsed:
                            results_tree.Collapse(tid_pak)
                            has_been_collapsed = True

                # Check Interrupt
                if self._stop_event.is_set():
                    break

           # Check Interrupt
            if self._stop_event.is_set():
                self._gui.on_search_cancelled()
                break
            else:
                self._gui.on_pak_processed(pak_name)


        # ===================================================================================================
        # Success - Search Finished
        # ===================================================================================================
        if not self.was_stopped():
            self._gui.on_search_success()


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
    # Setters
    # ===================================================================================================
    def set_auto_expand(self, auto_expand):
        '''
        Sets the auto-expand state

        :param auto_expand: The new auto-expand state
        :type auto_expand: bool
        '''
        self._auto_expand = auto_expand

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


