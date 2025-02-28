# ===================================================================================================
# Imports: External
# ===================================================================================================
import re

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .pak_asset_types import *

# ===================================================================================================
# PAK Asset Class
# ===================================================================================================
class PAKAsset:
    '''
    PAK Asset. Represents a file within a PAK archive
    '''

    # ===================================================================================================
    # Properties
    # ===================================================================================================

    # ===================================================================================================
    # Methods
    # ===================================================================================================
    def __init__(self, pak, path):
        '''
        Constructor

        :param pak: The PAK File that the Asset belongs to
        :type pak: PAKFile
        :param path: The asset's path within the PAK File
        :type path: str
        '''
        self._pak = pak
        self._path = path
        self._path_sections = []
        self._asset_type = None
        self._filename = None
        self._dir = None

    # ===================================================================================================
    # Getters
    # ===================================================================================================
    def get_path(self):
        '''
        Gets the Asset's path relative to the PAK File

        :return: The asset's path
        :rtype: str
        '''
        return self._path

    def get_dir(self):
        '''
        Gets the asset's directory. Effectively its path, minus the asset filename
        :return:
        '''
        if not self._dir:
            self._dir = "/".join(self.get_path_sections()[:-1])
        return self._dir

    def get_pak(self):
        '''
        Gets the PAKFile that this asset belongs to

        :return: The parent PAKFile, or None of this asset has no parent
        :rtype: PAKFile | None
        '''
        return self._pak

    def get_path_sections(self):
        '''
        Gets the PAK Asset's path split into sections, e.g. test/testing/123 -> ["test", "testing", "123]

        :return: The asset path in sections
        :rtype: list[str]
        '''
        if not self._path_sections:
            self._path_sections = self.get_path().split("/")
        return self._path_sections

    def get_filename(self):
        '''
        Gets the asset's filename

        :return: The asset's filename
        :rtype: str
        '''
        if not self._filename:
            self._filename = self.get_path().split("/")[-1]
        return self._filename

    def get_asset_type(self):
        '''
        Gets the asset's type

        :return: The asset's type
        :rtype: str
        '''

        if not self._asset_type:
            asset_name = self.get_filename().lower()

            # ===================================================================================================
            # Asset Matchers
            # ===================================================================================================
            # Asset - Material
            if asset_name.endswith(".mtl"):
                self._asset_type = ASSET_MATERIAL
            # Asset - Texture
            elif re.match(".*\.dds(\.\d+)*$", asset_name):
                self._asset_type = ASSET_TEXTURE
            # Asset - Blend Space
            elif asset_name.endswith(".bspace"):
                self._asset_type = ASSET_BLEND_SPACE
            # Asset - CFG
            elif asset_name.endswith(".cgf"):
                self._asset_type = ASSET_CGF
            # Asset - Skin
            elif asset_name.endswith(".skin"):
                self._asset_type = ASSET_SKIN
            # Asset - XML
            elif asset_name.endswith(".xml"):
                self._asset_type = ASSET_XML
            # Asset - Audio
            elif asset_name.endswith(".ogg"):
                self._asset_type = ASSET_AUDIO
            # Asset - Flash
            elif asset_name.endswith(".gfx"):
                self._asset_type = ASSET_FLASH
            # Asset - Character Animations
            elif asset_name.endswith(".caf"):
                self._asset_type = ASSET_CHAR_ANIM
            # Asset - DBA
            elif asset_name.endswith(".dba"):
                self._asset_type = ASSET_DBA


        return self._asset_type

    def is_of_type(self, _type):
        '''
        Checks if the asset is of a specific type

        :param _type: The type to check for
        :type _type: str
        :return: True if asset is of the specified type, otherwise false
        :rtype: bool
        '''
        if self.get_asset_type() == _type:
            return True
        return False

