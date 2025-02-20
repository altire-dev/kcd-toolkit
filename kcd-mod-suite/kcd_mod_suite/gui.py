# ===================================================================================================
# Imports: External
# ===================================================================================================
import wx

import kcd_asset_finder
import kcd_mod_generator
import kcd_pak_builder
from kcd_pak_builder import KCDPakBuilderGui
from kcd_mod_generator import KCDModGeneratorGui
from kcd_asset_finder import KCDAssetFinderGui

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .abs_gui import ModSuiteMainFrame

# ===================================================================================================
# KCD Mod Suite GUI Class
# ===================================================================================================
class KCDModSuiteGui(ModSuiteMainFrame):
    '''
    Mod Suite GUI
    '''

    # ===================================================================================================
    # Properties
    # ===================================================================================================

    # ===================================================================================================
    # Methods
    # ===================================================================================================
    def __init__(self, version, author):
        '''
        Constructor
        '''
        self._version = version
        self._author = author

        super(KCDModSuiteGui, self).__init__(None)

        # Set Up UI
        self._init_ui()


    def _init_ui(self):
        '''
        Initialises and sets up the Mod Suite User Interface and Panels
        '''

        # ===================================================================================================
        # App Setup: KCD Mod Generator
        # ===================================================================================================
        mod_generator = KCDModGeneratorGui(
            kcd_mod_generator.VERSION,
            kcd_mod_generator.AUTHOR,
            suite=self
        )
        mod_generator.MainPanel.Reparent(self.Notebook)
        self.Notebook.AddPage(mod_generator.MainPanel, "Mod Generator")

        # ===================================================================================================
        # App Setup: KCD PAK Builder
        # ===================================================================================================
        pak_builder = KCDPakBuilderGui(
            kcd_pak_builder.VERSION,
            kcd_pak_builder.AUTHOR,
            suite=self
        )
        pak_builder.MainPanel.Reparent(self.Notebook)
        self.Notebook.AddPage(pak_builder.MainPanel, "PAK Builder")

        # ===================================================================================================
        # App Setup: KCD Asset Finder
        # ===================================================================================================
        asset_finder = KCDAssetFinderGui(
            kcd_asset_finder.VERSION,
            kcd_asset_finder.AUTHOR,
            suite=self
        )
        asset_finder.MainPanel.Reparent(self.Notebook)
        self.Notebook.AddPage(asset_finder.MainPanel, "Asset Finder")



